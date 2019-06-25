use crate::modules::sensors::SensorStatus;
use crate::modules::sensors::SensorTrait;
use crate::modules::sensors::SensorType;

pub struct Pressure {
    location: String,
}

impl Pressure {
    pub fn new(location: &str) -> Self {
        Pressure {
            location: String::from(location),
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
        SensorStatus::Safe
    }

    fn s_type(&self) -> SensorType {
        SensorType::Pressure
    }
}
