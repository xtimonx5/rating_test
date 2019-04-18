from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL("""         
DROP MATERIALIZED VIEW IF EXISTS leaderboard;
CREATE MATERIALIZED VIEW leaderboard
AS SELECT
     row_number() over (ORDER BY rr.rating desc, rr.datetime) as rate_place,
     rr.user_id,
     rr.rating,
     rr.datetime
   FROM common_raterecord rr ORDER BY rate_place;

CREATE UNIQUE INDEX rate_place_unique_id
  ON leaderboard (rate_place);"""),
    ]
