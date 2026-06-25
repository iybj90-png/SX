from src.quality_predictor import QualityPredictor
from src.synthetic_data import generate_batches, to_feature_matrix


def test_predictor_separates_normal_from_anomalous():
    batches = generate_batches(n=300, anomaly_rate=0.3, seed=1)
    x, y = to_feature_matrix(batches)

    predictor = QualityPredictor()
    predictor.fit(x, y)

    normal_x, _ = to_feature_matrix(generate_batches(n=20, anomaly_rate=0.0, seed=2))
    anomalous_x, _ = to_feature_matrix(generate_batches(n=20, anomaly_rate=1.0, seed=3))

    normal_probs = predictor.predict_pass_probability(normal_x)
    anomalous_probs = predictor.predict_pass_probability(anomalous_x)

    assert sum(normal_probs) / len(normal_probs) > sum(anomalous_probs) / len(anomalous_probs)
