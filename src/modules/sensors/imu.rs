use super::bno055::{BNO055, BNO055OperationMode};

use std::thread;
use std::time::Duration;

use i2cdev::core::*;
use i2cdev::linux::{LinuxI2CDevice, LinuxI2CError};

use super::{Sensor, SensorTrait};

pub struct IMU {
    sensor: Sensor,
}

impl SensorTrait for IMU {
    fn name(&self) -> &String {
        &self.sensor.name
    }
}


const IMU_ADDR: u16 = 0x28;

// real code should probably not use unwrap()
pub fn imu_test() {
    let mut dev = LinuxI2CDevice::new("/dev/i2c-1", IMU_ADDR).unwrap();
    let mut bno = BNO055::new(dev).unwrap();

    let some_millis = Duration::from_millis(500);

    println!("{:?}", bno.get_revision().unwrap());
    bno.set_mode(BNO055OperationMode::Ndof).unwrap();
    loop {
        let accel = bno.get_linear_acceleration().unwrap();
        println!("{:+2.2}\t{:+2.2}\t{:+2.2}", accel.x, accel.y, accel.z);
        thread::sleep(some_millis);

    }

}
