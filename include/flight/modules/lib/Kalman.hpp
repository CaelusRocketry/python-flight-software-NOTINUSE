#ifndef FLIGHT_KALMAN_HPP
#define FLIGHT_KALMAN_HPP

class Kalman {
private:
    double process_variance;
    double measurement_variance;
    double kalman_value;
    double sensor_value;
    double P;
    double K;

public:
    Kalman(double process_variance, double measurement_variance, double kalman_value);
    double update_kalman(double sensor_value_);
};
#endif //FLIGHT_KALMAN_HPP
