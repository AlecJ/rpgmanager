from datetime import datetime, timedelta
from util import session_scope
from model.db import RPGManagerCampaign

def remove_stale_rpgmanager_campaigns():
    """
    The criteria for a stale campaign is one that:
    - is a day old and has no players
    - hasn't been viewed in four months
    """
    with session_scope() as session:
        # day old and no players
        day_ago = datetime.now() - timedelta(days=1)
        # stale_campaigns = session.query(RPGManagerCampaign).filter(RPGManagerCampaign.last_read_time < day_ago).filter().all()

        # last read > 120 days old
        four_months_ago = datetime.now() - timedelta(days=120)
        stale_campaigns = session.query(RPGManagerCampaign).filter(RPGManagerCampaign.last_read_time < four_months_ago).all()
        for c in stale_campaigns:
            session.delete(c)
        session.commit()
