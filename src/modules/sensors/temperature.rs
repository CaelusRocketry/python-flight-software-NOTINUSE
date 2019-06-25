extern crate rand;

use chrono::prelude::*;
use priority_queue::PriorityQueue;
use rand::Rng;

use crate::modules::sensors::SensorStatus;
use crate::modules::sensors::SensorTrait;
use crate::modules::sensors::SensorType;
use crate::modules::telemetry::logging::{Level, Log};

pub struct Temperature {
    location: String,
    log: PriorityQueue<Log, usize>,
    // Unit: K
    TEMP_STATUS_WARN: f32,
    // Unit: K
    TEMP_STATUS_CRIT: f32,
}

impl Temperature {
    pub fn new(location: &str, temp_status_warn: f32, temp_status_crit: f32) -> Self {
        Temperature {
            location: String::from(location),
            log: PriorityQueue::new(),
            TEMP_STATUS_WARN: temp_status_warn,
            TEMP_STATUS_CRIT: temp_status_crit,
        }
    }

    pub fn temp(&mut self) -> f32 {
        let mut rng = rand::thread_rng();
        rng.gen_range(200.0, 400.0)
    }

    fn check_temp(&mut self) -> SensorStatus {
        let temp = self.temp();
        let status: SensorStatus;

        if temp > self.TEMP_STATUS_CRIT {
            status = SensorStatus::Crit;
        } else if temp > self.TEMP_STATUS_WARN {
            status = SensorStatus::Warn;
        } else {
            status = SensorStatus::Safe;
        }

        let log = Log {
            message: format!("{} K", &temp.to_string()),
            timestamp: Utc::now(),
            sender: self.name(),
            level: Level::sensor_status_to_level(&status),
        };

        self.log.push(log, 5);

        status
    }
}

impl SensorTrait for Temperature {
    fn name(&self) -> String {
        let result = format!("{: ^16}", format!("TEMP.{}", &self.location()));
        result.to_ascii_uppercase()
    }

    fn location(&self) -> &String {
        &self.location
    }

    fn status(&mut self) -> SensorStatus {
        self.check_temp()
    }

    fn s_type(&self) -> SensorType {
        SensorType::Temperature
    }

    fn log(&mut self) -> &mut PriorityQueue<Log, usize> {
        &mut self.log
    }
}
