extern crate rand;

use chrono::prelude::*;
use priority_queue::PriorityQueue;
use rand::Rng;

use crate::modules::sensors::SensorStatus;
use crate::modules::sensors::SensorTrait;
use crate::modules::sensors::SensorType;
use crate::modules::telemetry::logging::{Level, Log};

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
        let pressure = self.pressure();
        let status: SensorStatus;

        if pressure > self.PRESSURE_STATUS_CRIT {
            status = SensorStatus::Crit;
        } else if pressure > self.PRESSURE_STATUS_WARN {
            status = SensorStatus::Warn;
        } else {
            status = SensorStatus::Safe;
        }

        let log = Log {
            message: format!("{} mPa", &pressure.to_string()),
            timestamp: Utc::now(),
            sender: self.name(),
            level: Level::sensor_status_to_level(&status),
        };

        self.log.push(log, 5);

        status
    }
}

impl SensorTrait for Pressure {
    fn name(&self) -> String {
        let result = format!("{: ^16}", format!("PRESSURE.{}", &self.location()));
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
