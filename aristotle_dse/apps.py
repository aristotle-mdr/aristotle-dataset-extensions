from aristotle_mdr.apps import AristotleExtensionBaseConfig


class AristotleDSEConfig(AristotleExtensionBaseConfig):
    name = 'aristotle_dse'
    verbose_name = "Aristotle Dataset Extensions"
    description = "Aristotle Dataset Extensions adds content types for tracking data set defintions and data sources."
