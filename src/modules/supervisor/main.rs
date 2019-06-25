use std::thread;
use std::time::Duration;

use crate::modules::sensors::imu::IMU;
use crate::modules::sensors::pressure::Pressure;
use crate::modules::sensors::temperature::Temperature;
use crate::modules::sensors::SensorTrait;

pub fn start() {
    // Initialize sensors
    let mut sensors: [Box<SensorTrait>; 3] = [
        Box::new(IMU::new("NOSECONE", 0x28)),
        Box::new(Pressure::new("TANK", 1.75, 2.0)),
        Box::new(Temperature::new("TANK", 350.0, 400.0)),
    ];

    // Main loop
    loop {
        println!("{:?}", sensors[1].as_mut().status());
        thread::sleep(Duration::from_millis(500));
    }
}
