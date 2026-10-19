"""Static figures drawn solely from the observation table used in the calculation."""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def scatter(observations, predictor: str, outcome: str, path) -> None:
    """Plot every paired observation without fitting an additional model."""
    figure, axis = plt.subplots(figsize=(7, 5), layout="constrained")
    axis.scatter(observations[predictor], observations[outcome], color="#2b5d80", s=20)
    for unit_id, row in observations.iterrows():
        axis.annotate(
            str(unit_id),
            (row[predictor], row[outcome]),
            fontsize=6,
            xytext=(2, 2),
            textcoords="offset points",
        )
    axis.set(xlabel=predictor, ylabel=outcome, title=f"{outcome} and {predictor}")
    path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(path, dpi=140, metadata={"Software": "open-reanalysis"})
    plt.close(figure)
