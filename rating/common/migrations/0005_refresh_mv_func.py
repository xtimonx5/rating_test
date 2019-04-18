from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('common', '0004_auto_20190416_0859'),
    ]

    operations = [
        migrations.RunSQL("""
CREATE OR REPLACE FUNCTION refresh_leaderboard_mv() RETURNS int AS
  $BODY$
    BEGIN
      IF NOT EXISTS(SELECT * FROM pg_stat_activity where query='SELECT refresh_leaderboard_mv();') THEN
        RAISE NOTICE 'MV refreshing is started';
        EXECUTE 'REFRESH MATERIALIZED VIEW CONCURRENTLY leaderboard;';
      END IF;
      RETURN NULL;
    END;
  $BODY$
LANGUAGE plpgsql VOLATILE
COST 100;
"""),
    ]
