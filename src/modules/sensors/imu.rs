use super::{Sensor, SensorTrait};

pub struct IMU {
    sensor: Sensor,
}

impl SensorTrait for IMU {
    fn name(&self) -> &String {
        &self.sensor.name
    }
}

pub fn imu_test() {
    println!("Testing IMU");
    let i = IMU {
        sensor: Sensor {
            name: String::from("An IMU"),
            safe_val: 10,
            warn_val: 15,
            crit_val: 20,
        },
    };
    println!("{}", i.name());
}
