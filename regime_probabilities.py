import math
import numpy as np


def norm_cdf(x):
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def markov_regime_weights(n_steps, initial_probs, transition_matrix):
    """
    Returns weights[k] = probability of spending exactly k periods in regime 0
    and n_steps-k periods in regime 1.

    Convention:
    - initial_probs is the probability of the regime for the first return step.
    - transition_matrix[i, j] = P(next regime = j | current regime = i).
    """

    initial_probs = np.asarray(initial_probs, dtype=float)
    P = np.asarray(transition_matrix, dtype=float)

    if n_steps < 1:
        raise ValueError("n_steps must be >= 1")

    # dp[state, k] after current step
    dp = np.zeros((2, n_steps + 1))

    # First return step
    dp[0, 1] = initial_probs[0]
    dp[1, 0] = initial_probs[1]

    for _ in range(1, n_steps):
        new_dp = np.zeros_like(dp)

        for prev_state in range(2):
            for k in range(n_steps + 1):
                prob = dp[prev_state, k]
                if prob == 0.0:
                    continue

                for next_state in range(2):
                    new_k = k + (1 if next_state == 0 else 0)
                    new_dp[next_state, new_k] += prob * P[prev_state, next_state]

        dp = new_dp

    # Sum over final regime
    return dp.sum(axis=0)


def terminal_price_cdf(
    x,
    s0,
    n_steps,
    dt,
    mu,
    sigma,
    initial_probs,
    transition_matrix,
):
    """
    CDF P(S_T <= x) under a 2-state Markov regime-switching GBM.
    """

    if x <= 0:
        return 0.0

    mu = np.asarray(mu, dtype=float)
    sigma = np.asarray(sigma, dtype=float)

    weights = markov_regime_weights(
        n_steps=n_steps,
        initial_probs=initial_probs,
        transition_matrix=transition_matrix,
    )

    drift = (mu - 0.5 * sigma ** 2) * dt
    var = sigma ** 2 * dt

    log_x = math.log(x)
    log_s0 = math.log(s0)

    total = 0.0

    for k, w in enumerate(weights):
        if w == 0.0:
            continue

        n0 = k
        n1 = n_steps - k

        mean = log_s0 + n0 * drift[0] + n1 * drift[1]
        variance = n0 * var[0] + n1 * var[1]
        std = math.sqrt(variance)

        total += w * norm_cdf((log_x - mean) / std)

    return total


def terminal_price_percentile(
    p,
    s0,
    n_steps,
    dt,
    mu,
    sigma,
    initial_probs,
    transition_matrix,
    tol=1e-10,
    max_iter=200,
):
    """
    Finds S_p such that P(S_T <= S_p) = p.
    Uses bisection.
    """

    if not 0.0 < p < 1.0:
        raise ValueError("p must be between 0 and 1")

    mu = np.asarray(mu, dtype=float)
    sigma = np.asarray(sigma, dtype=float)

    # Conservative initial bracket
    worst_drift = min(mu - 0.5 * sigma ** 2)
    best_drift = max(mu - 0.5 * sigma ** 2)
    max_vol = max(sigma)

    low = s0 * math.exp(worst_drift * n_steps * dt - 10.0 * max_vol * math.sqrt(n_steps * dt))
    high = s0 * math.exp(best_drift * n_steps * dt + 10.0 * max_vol * math.sqrt(n_steps * dt))

    for _ in range(max_iter):
        mid = 0.5 * (low + high)

        cdf_mid = terminal_price_cdf(
            mid,
            s0,
            n_steps,
            dt,
            mu,
            sigma,
            initial_probs,
            transition_matrix,
        )

        if cdf_mid < p:
            low = mid
        else:
            high = mid

        if high - low < tol * max(1.0, mid):
            break

    return 0.5 * (low + high)


def expected_max_drawdown_markov_gbm(
    s0,
    n_steps,
    dt,
    mu,
    sigma,
    initial_probs,
    transition_matrix,
    n_paths=100_000,
    seed=42,
):
    rng = np.random.default_rng(seed)

    mu = np.asarray(mu, dtype=float)
    sigma = np.asarray(sigma, dtype=float)
    initial_probs = np.asarray(initial_probs, dtype=float)
    p = np.asarray(transition_matrix, dtype=float)

    states = np.empty((n_paths, n_steps), dtype=np.int8)
    states[:, 0] = rng.choice(2, size=n_paths, p=initial_probs)

    u = rng.random((n_paths, n_steps - 1))

    for t in range(1, n_steps):
        prev = states[:, t - 1]
        states[:, t] = (u[:, t - 1] >= p[prev, 0]).astype(np.int8)

    z = rng.standard_normal((n_paths, n_steps))

    log_returns = (
        (mu[states] - 0.5 * sigma[states] ** 2) * dt
        + sigma[states] * np.sqrt(dt) * z
    )

    log_prices = np.cumsum(log_returns, axis=1)
    prices = s0 * np.exp(log_prices)

    prices = np.concatenate(
        [np.full((n_paths, 1), s0), prices],
        axis=1,
    )

    running_max = np.maximum.accumulate(prices, axis=1)
    drawdowns = prices / running_max - 1.0

    max_drawdowns = drawdowns.min(axis=1)

    return {
        "expected_mdd": max_drawdowns.mean(),
        "median_mdd": np.percentile(max_drawdowns, 50),
        "p01_mdd": np.percentile(max_drawdowns, 1),
        "p05_mdd": np.percentile(max_drawdowns, 5),
        "p95_mdd": np.percentile(max_drawdowns, 95),
        "p99_mdd": np.percentile(max_drawdowns, 99),
    }


s0 = 100.0
n_steps = 252
dt = 1.0 / 252.0

# Regime 0: expansion
# Regime 1: recession
mu = [0.12, -0.08]
sigma = [0.16, 0.32]

initial_probs = [0.80, 0.20]

transition_matrix = [
    [0.97, 0.03],
    [0.08, 0.92],
]

for p in [0.01, 0.05, 0.50, 0.95, 0.99]:
    q = terminal_price_percentile(
        p,
        s0,
        n_steps,
        dt,
        mu,
        sigma,
        initial_probs,
        transition_matrix,
    )
    print(f"{p:5.1%}: {q:.2f}")

result = expected_max_drawdown_markov_gbm(
    s0=100.0,
    n_steps=252,
    dt=1.0 / 252.0,
    mu=[0.12, -0.08],
    sigma=[0.16, 0.32],
    initial_probs=[0.80, 0.20],
    transition_matrix=[
        [0.97, 0.03],
        [0.08, 0.92],
    ],
)

for k, v in result.items():
    print(f"{k}: {v:.2%}")
