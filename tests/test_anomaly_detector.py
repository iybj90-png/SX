from src.anomaly_detector import ProcessAnomalyDetector
from src.synthetic_data import generate_batches, to_feature_matrix


def test_detector_flags_anomalous_sample():
    normal_x, _ = to_feature_matrix(generate_batches(n=200, anomaly_rate=0.0, seed=1))

    detector = ProcessAnomalyDetector(contamination=0.05)
    detector.fit(normal_x)

    anomalous_x, _ = to_feature_matrix(generate_batches(n=1, anomaly_rate=1.0, seed=2))
    normal_sample_x, _ = to_feature_matrix(generate_batches(n=1, anomaly_rate=0.0, seed=3))

    assert detector.is_anomalous(anomalous_x[0]) is True
    assert detector.is_anomalous(normal_sample_x[0]) is False
