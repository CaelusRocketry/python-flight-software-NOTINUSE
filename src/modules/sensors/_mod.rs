pub mod imu;
pub mod bno055;

pub struct Sensor {
    pub name: String,
    pub safe_val: i16,
    pub warn_val: i16,
    pub crit_val: i16,
}

pub trait SensorTrait {
    fn name(&self) -> &String;
}
