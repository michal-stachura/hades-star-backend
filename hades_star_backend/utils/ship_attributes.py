class ShipAttribute:

    attributes = {
        "weapon": [
            ("BATTERY", "Battery"),
            ("LASER", "Laser"),
            ("MASS_BATTERY", "Mass Battery"),
            ("DUAL_LASER", "Dual Laser"),
            ("BARRAGE", "Barrage"),
            ("DART_LAUNCHER", "Dart Launcher"),
        ],
        "shield": [
            ("DELTA_SHIELD", "Delta Shield"),
            ("PASSIVE_SHIELD", "Passive Shield"),
            ("OMEGA_SHIELD", "Omega Shield"),
            ("MIRROR_SHIELD", "Mirror Shield"),
            ("BLAST_SHIELD", "Blast Shield"),
            ("AREA_SHIELD", "Area Shield"),
        ],
        "support": [
            ("EMP", "Emp"),
            ("TELEPORT", "Teleport"),
            ("RED_STAR_LIFE_EXTENDER", "Red Star life extender"),
            ("REMOTE_REPAIR", "Remote repair"),
            ("TIME_WRAP", "Time Warp"),
            ("UNITY", "Unity"),
            ("SANCTUARY", "Sanctuary"),
            ("STEALTH", "Stealth"),
            ("FORTIFY", "Fortify"),
            ("IMPULSE", "Impulse"),
            ("ALPHA_ROCKET", "Alpha rocket"),
            ("SALVAGE", "Salvage"),
            ("SUPRESS", "Suppress"),
            ("DESTINY", "Destiny"),
            ("BARRIER", "Barrier"),
            ("VENEGANCE", "Venegeance"),
            ("DELTA_ROCKET", "Delta rocket"),
            ("LEAP", "Leap"),
            ("BOND", "Bond"),
            ("LASER_TURRET", "Laser turret"),
            ("ALPHA_DRONE", "Alpha drone"),
            ("SUSPEND", "Suspend"),
            ("OMEGA_ROCKET", "Omega rocket"),
            ("REMOTE_BOMB", "Remote bomb"),
        ],
        "mining": [
            ("MINING_BOOST", "Mining boost"),
            ("HYDROGEN_BAY_EXTENSION", "Hydrogen Bay extension"),
            ("ENRICH", "Enrich"),
            ("REMOTE_MINING", "Remote mining"),
            ("HYDROGEN_UPLOAD", "Hydrogen upload"),
            ("MINING_UNITY", "Mining unity"),
            ("CRUNCH", "Crunch"),
            ("GENESIS", "Genesis"),
            ("HYDROGEN_ROCKET", "Hydrogen rocket"),
            ("MINING_DRONE", "Mining drone"),
        ],
        "trade": [
            ("CARGO_BAY_EXTENSION", "Cargo Bay Extension"),
            ("SHIPMENT_COMPUTER", "Shipment Computer"),
            ("TRADE_BOOST", "Trade Boost"),
            ("RUSH", "Rush"),
            ("TRADE_BURST", "Trade Burst"),
            ("SHIPMENT_DRONE", "Shipment Drone"),
            ("OFFLOAD", "Offload"),
            ("SHIPMENT_BEAM", "Shipment Beam"),
            ("ENTRUST", "Entrust"),
            ("DISPATCH", "Dispatch"),
            ("RECALL", "Recall"),
            ("RELIC_DRONE", "Relic Drone"),
        ],
    }

    def __init__(self, group_name: str | None = None) -> None:
        if group_name:
            self.group_name = group_name

    def __convert_attribute_to_dict(self, attribute):
        return {
            "id": attribute[0],
            "name": attribute[1],
            "max": self.get_maximum_value(attribute[0]),
            "set": 0,
        }

    def find_group_name_by_attribute_name(self, attribute_name: str) -> str | None:
        for key in self.attributes.keys():
            test = list(filter(lambda x: x[0] == attribute_name, self.attributes[key]))
            if len(test) > 0:
                return key
        return None

    def get_attributes(self) -> tuple:
        return self.attributes[self.group_name]

    def get_default_attribute(self) -> str:
        return self.attributes[self.group_name][0][0]

    def get_attribure_index(self, attribute_name: str) -> int:
        attributes = self.get_attributes()
        return [x[0] for x in attributes].index(attribute_name)

    def get_maximum_value(self, attribute_name: str) -> int:
        if attribute_name in ["SANCTUARY", "RECALL"]:
            return 1
        elif attribute_name in [
            "RED_STAR_LIFE_EXTENDER",
            "LEAP",
            "OFFLOAD",
            "DISPATCH",
            "HYDROGEN_BAY_EXTENSION",
            "REMOTE_MINING",
            "MINING_UNITY",
            "MINING_DRONE",
        ]:
            return 10
        else:
            return 12

    def get_attributes_json_dict(self) -> dict:
        attributes_dict = {}

        for key in self.attributes.keys():
            self.group_name = key
            attributes_dict[key] = map(
                self.__convert_attribute_to_dict, self.get_attributes()
            )

        return attributes_dict
