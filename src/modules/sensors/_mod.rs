pub mod imu;
pub mod pressure;

// Statuses that sensors have, based on the sensor readings
#[derive(Debug)]
pub enum SensorStatus {
    Safe,
    Warn,
    Crit,
}

pub enum SensorType {
    Temperature,
    Pressure,
    IMU,
}

pub trait SensorTrait {
    fn name(&self) -> String;
    fn location(&self) -> &String;
    fn status(&mut self) -> SensorStatus;
    // Can't use `type` because it's a reserved keyword
    fn s_type(&self) -> SensorType;
}
