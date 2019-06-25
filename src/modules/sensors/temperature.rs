extern crate rand;

use rand::Rng;

use crate::modules::sensors::SensorStatus;
use crate::modules::sensors::SensorTrait;
use crate::modules::sensors::SensorType;

pub struct Temperature {
    location: String,
    // Unit: K
    TEMP_STATUS_WARN: f32,
    // Unit: K
    TEMP_STATUS_CRIT: f32,
}

impl Temperature {
    pub fn new(location: &str, temp_status_warn: f32, temp_status_crit: f32) -> Self {
        Temperature {
            location: String::from(location),
            TEMP_STATUS_WARN: temp_status_warn,
            TEMP_STATUS_CRIT: temp_status_crit,
        }
    }

    pub fn temp(&mut self) -> f32 {
        let mut rng = rand::thread_rng();
        rng.gen_range(200.0, 400.0)
    }

    fn check_temp(&mut self) -> SensorStatus {
        if self.temp() > self.TEMP_STATUS_CRIT {
            SensorStatus::Crit
        } else if self.temp() > self.TEMP_STATUS_WARN {
            SensorStatus::Warn
        } else {
            SensorStatus::Safe
        }
    }
}

impl SensorTrait for Temperature {
    fn name(&self) -> String {
        let result = String::new() + "Temperature" + "." + &self.location();
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
}
