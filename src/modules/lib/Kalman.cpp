//
// Created by adiv413 on 4/27/2020.
//

#include <flight/modules/lib/Kalman.hpp>

Kalman::Kalman(double process_variance, double measurement_variance, double kalman_value) {
    this->process_variance = process_variance * process_variance;
    this->measurement_variance = measurement_variance * measurement_variance;
    this->kalman_value = kalman_value;
    this->sensor_value = kalman_value;
    this->P = 1.0;
    this->K = 1.0;
}

double Kalman::update_kalman(double sensor_value_) {
    this->P += this->process_variance;
    this->K = this->P / (this->P + this->measurement_variance);
    this->kalman_value = this->K * sensor_value_ + (1 - this->K) * this->kalman_value;
    this->P *= (1 - this->K);

    return this->kalman_value;
}