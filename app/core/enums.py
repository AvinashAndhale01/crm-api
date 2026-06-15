from enum import Enum


class RoleType(str, Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    SALES_REP = "sales_rep"


class LeadStatus(str, Enum):
    INITIAL_CONTACT = "initial_contact"
    COLD = "cold"
    WARM = "warm"
    HOT = "hot"
    WON = "won"
    NEGOTIATION = "nigotiation"
    PROSPECT = "prospect"
    LOST = "lost"
    QUALIFIED = "qualified"
    FOLLOW_UP = "follow_up"


class LeadSource(str, Enum):
    WEBSITE = "website"
    GOOGLE_ADS = "google_ads"
    FACEBOOK_ADS = "facebook_ads"
    WEBSITE = "website"
    REFERRAL = "referral"
    EMAIL = "email"
    SOCIAL_MEDIA = "social_media"
    TRADE_SHOW = "trade_show"
