//
// Created by adiv413 on 4/26/2020.
//

#include <cmath>

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
    Kalman(double process_variance, double measurement_variance, double kalman_value) {
        this->process_variance = process_variance * process_variance;
        this->measurement_variance = measurement_variance * measurement_variance;
        this->kalman_value = kalman_value;
        this->sensor_value = kalman_value;
        this->P = 1.0;
        this->K = 1.0;
    }

    double update_kalman(double sensor_value) {
        this->P += this->process_variance;
        this->K = this->P / (this->P + this->measurement_variance);
        this->kalman_value = this->K * sensor_value + (1 - this->K) * this->kalman_value;
        this->P *= (1 - this->K);

        return this->kalman_value;
    }
};
#endif //FLIGHT_KALMAN_HPP
