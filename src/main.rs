#[path = "modules/_mod.rs"]
mod modules;

//use std::thread;
//use std::time::Duration;

// use crate::modules::sensors::SensorTrait;
/*
fn main() {
    let mut imu = modules::sensors::imu::IMU::new("NOSECONE", 0x28);

    let delay = Duration::from_millis(100);

    println!("{}:", imu.name());
    loop {
        let acc = imu.acc();
        let gyro = imu.gyro();
        println!("Acceleration:\t{:+2.2}\t{:+2.2}\t{:+2.2}", acc.0, acc.1, acc.2);
        println!("Gyroscope:\t{:+2.2}\t{:+2.2}\t{:+2.2}", gyro.0, gyro.1, gyro.2);
        thread::sleep(delay);
    }
}
*/

fn main() {
    modules::telemetry::telem::runsocket();
}
