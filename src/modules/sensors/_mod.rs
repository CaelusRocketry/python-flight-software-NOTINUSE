pub mod imu;

// Statuses that sensors have, based on the sensor readings
pub enum SensorStatus {
    Safe,
    Warn,
    Crit,
}

pub enum SensorType {
    Temperature,
    Pressure,
    IMU
}

pub trait SensorTrait {
    fn name(&self) -> &String;
    fn status(&self) -> SensorStatus;
    fn type(&self) -> SensorType;
}
