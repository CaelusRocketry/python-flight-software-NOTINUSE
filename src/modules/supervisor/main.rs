use std::thread;
use std::time::Duration;

use priority_queue::PriorityQueue;

use crate::modules::sensors::imu::IMU;
use crate::modules::sensors::pressure::Pressure;
use crate::modules::sensors::temperature::Temperature;
use crate::modules::sensors::SensorStatus;
use crate::modules::sensors::SensorTrait;
use crate::modules::telemetry::logging::Log;

pub fn start() {
    // Initialize sensors
    let mut sensors: [Box<SensorTrait>; 3] = [
        Box::new(IMU::new("NOSECONE", 0x28)),
        Box::new(Pressure::new("TANK", 1.75, 2.0)),
        Box::new(Temperature::new("TANK", 350.0, 400.0)),
    ];

    let delay_time: i8 = 100;
    let delay: Duration = Duration::from_millis(100);

    // Main loop
    loop {
        for sensor in &mut sensors {
            let sensor_status: SensorStatus = sensor.as_mut().status();
            let sensor_log: &mut PriorityQueue<Log, usize> = sensor.as_mut().log();
            match sensor_log.pop() {
                Some(log_tuple) => println!("{}", log_tuple.0),
                _ => (),
            }
        }

        thread::sleep(delay);
    }
}
