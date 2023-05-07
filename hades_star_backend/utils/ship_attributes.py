class ShipAttribute:

    attributes = {
        "Weapon": [
            ("BATTERY", "Battery", "battery"),
            ("LASER", "Laser", "laser"),
            ("MASS_BATTERY", "Mass Battery", "mass"),
            ("DUAL_LASER", "Dual Laser", "dual"),
            ("BARRAGE", "Barrage", "barrage"),
            ("DART_LAUNCHER", "Dart Launcher", "dart"),
        ],
        "Shield": [
            ("DELTA_SHIELD", "Delta Shield", "delta"),
            ("PASSIVE_SHIELD", "Passive Shield", "passive"),
            ("OMEGA_SHIELD", "Omega Shield", "omega"),
            ("MIRROR_SHIELD", "Mirror Shield", "mirror"),
            ("BLAST_SHIELD", "Blast Shield", "blast"),
            ("AREA_SHIELD", "Area Shield", "area"),
        ],
        "Support": [
            ("EMP", "Emp", "emp"),
            ("TELEPORT", "Teleport", "teleport"),
            ("RED_STAR_LIFE_EXTENDER", "Red Star life extender", "rsextender"),
            ("REMOTE_REPAIR", "Remote repair", "repair"),
            ("TIME_WRAP", "Time Warp", "warp"),
            ("UNITY", "Unity", "unity"),
            ("SANCTUARY", "Sanctuary", "sanctuary"),
            ("STEALTH", "Stealth", "stealth"),
            ("FORTIFY", "Fortify", "fortify"),
            ("IMPULSE", "Impulse", "impulse"),
            ("ALPHA_ROCKET", "Alpha rocket", "rocket"),
            ("SALVAGE", "Salvage", "salvage"),
            ("SUPRESS", "Suppress", "suppress"),
            ("DESTINY", "Destiny", "destiny"),
            ("BARRIER", "Barrier", "barrier"),
            ("VENEGANCE", "Venegeance", "vengeance"),
            ("DELTA_ROCKET", "Delta rocket", "deltarocket"),
            ("LEAP", "Leap", "leap"),
            ("BOND", "Bond", "bond"),
            ("LASER_TURRET", "Laser turret", "laserturret"),
            ("ALPHA_DRONE", "Alpha drone", "alphadrone"),
            ("SUSPEND", "Suspend", "suspend"),
            ("OMEGA_ROCKET", "Omega rocket", "omegarocket"),
            ("REMOTE_BOMB", "Remote bomb", "remotebomb"),
        ],
        "Mining": [
            ("MINING_BOOST", "Mining boost", "miningboost"),
            ("HYDROGEN_BAY_EXTENSION", "Hydrogen Bay extension", "hydrobay"),
            ("ENRICH", "Enrich", "enrich"),
            ("REMOTE_MINING", "Remote mining", "remote"),
            ("HYDROGEN_UPLOAD", "Hydrogen upload", "hydroupload"),
            ("MINING_UNITY", "Mining unity", "miningunity"),
            ("CRUNCH", "Crunch", "crunch"),
            ("GENESIS", "Genesis", "genesis"),
            ("HYDROGEN_ROCKET", "Hydrogen rocket", "hydrorocket"),
            ("MINING_DRONE", "Mining drone", "minedrone"),
        ],
        "Trade": [
            ("CARGO_BAY_EXTENSION", "Cargo Bay Extension", "cargobay"),
            ("SHIPMENT_COMPUTER", "Shipment Computer", "computer"),
            ("TRADE_BOOST", "Trade Boost", "tradeboost"),
            ("RUSH", "Rush", "rush"),
            ("TRADE_BURST", "Trade Burst", "tradeburst"),
            ("SHIPMENT_DRONE", "Shipment Drone", "shipdrone"),
            ("OFFLOAD", "Offload", "offload"),
            ("SHIPMENT_BEAM", "Shipment Beam", "beam"),
            ("ENTRUST", "Entrust", "entrust"),
            ("DISPATCH", "Dispatch", "dispatch"),
            ("RECALL", "Recall", "recall"),
            ("RELIC_DRONE", "Relic Drone", "relicdrone"),
        ],
    }

    def __init__(self, group_name: str | None = None) -> None:
        self.group_name = group_name
        self.all_keys = self.attributes.keys()

    def __convert_attribute_to_dict(self, attribute):
        return {
            "id": attribute[0],
            "name": attribute[1],
            "max": self.get_maximum_value(attribute[0]),
            "set": 0,
        }

    def find_group_name_by_attribute_name(self, attribute_name: str) -> str | None:
        for key in self.all_keys:
            test = list(filter(lambda x: x[0] == attribute_name, self.attributes[key]))
            if len(test) > 0:
                return key
        return None

    def get_attributes(self, group_name: str, with_hsc_id: bool = False) -> tuple:
        attributes = []

        if not with_hsc_id:
            attributes += [(attr[0], attr[1]) for attr in self.attributes[group_name]]
        else:
            attributes += [attr for attr in self.attributes[group_name]]

        return attributes

    def get_default_attribute(
        self,
        group_name: str,
    ) -> str:
        return self.attributes[group_name][0][0]

    def get_attribute_index(self, group_name: str, attribute_name: str) -> int:
        attributes = self.get_attributes(group_name)
        return [x[0] for x in attributes].index(attribute_name)

    def get_attribute(self, group_name: str, attribute_name: str) -> tuple:
        attributes = self.get_attributes(group_name, with_hsc_id=True)
        index = self.get_attribute_index(group_name, attribute_name)

        return attributes[index]

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
                self.__convert_attribute_to_dict, self.get_attributes(key)
            )

        return attributes_dict

    def get_all_keys(self) -> list:
        return self.all_keys
