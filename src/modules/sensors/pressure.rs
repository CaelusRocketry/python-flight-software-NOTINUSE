extern crate rand;

use priority_queue::PriorityQueue;
use rand::Rng;

use crate::modules::sensors::SensorStatus;
use crate::modules::sensors::SensorTrait;
use crate::modules::sensors::SensorType;
use crate::modules::telemetry::logging::{Log, Level};

pub struct Pressure {
    location: String,
    log: PriorityQueue<Log, usize>,
    // Unit: mPa
    PRESSURE_STATUS_WARN: f32,
    // Unit: mPa,
    PRESSURE_STATUS_CRIT: f32,
}

impl Pressure {
    pub fn new(location: &str, pressure_status_warn: f32, pressure_status_crit: f32) -> Self {
        Pressure {
            location: String::from(location),
            log: PriorityQueue::new(),
            PRESSURE_STATUS_WARN: pressure_status_warn,
            PRESSURE_STATUS_CRIT: pressure_status_crit,
        }
    }

    pub fn pressure(&mut self) -> f32 {
        let mut rng = rand::thread_rng();
        rng.gen_range(1.0, 2.0)
    }

    fn check_pressure(&mut self) -> SensorStatus {
        if self.pressure() > self.PRESSURE_STATUS_CRIT {
            SensorStatus::Crit
        } else if self.pressure() > self.PRESSURE_STATUS_WARN {
            SensorStatus::Warn
        } else {
            SensorStatus::Safe
        }
    }
}

impl SensorTrait for Pressure {
    fn name(&self) -> String {
        let result = String::new() + "Pressure" + "." + &self.location();
        result.to_ascii_uppercase()
    }

    fn location(&self) -> &String {
        &self.location
    }

    fn status(&mut self) -> SensorStatus {
        self.check_pressure()
    }

    fn s_type(&self) -> SensorType {
        SensorType::Pressure
    }

    fn log(&mut self) -> &mut PriorityQueue<Log, usize> {
        &mut self.log
    }
}
