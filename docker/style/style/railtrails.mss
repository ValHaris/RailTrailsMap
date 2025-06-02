/* For the main linear features, such as roads and railways. */
@railtrail:rgb(60, 199, 187);
@railtrail-badtrack:rgb(103, 113, 199);
@railtrail-width: 8;
@railtrail-inner-width: 6;
@warning: rgb(221, 80, 14);

@offrailtrail:rgba(112, 150, 146, 0.7);
@offrailtrail-width: 5;

#railtrails {
  [zoom >= 4] {
    line/line-color: @railtrail;
    line/line-join: round;
    line/line-cap: round;
    line/line-width: @railtrail-width;

    /* note that railway = railtrail is synthesized in the LUA import filter */
    [railway != 'abandoned'][railway != 'disused'][railway != 'razed'][railway != 'railtrail'] {
      /* this should apply when a route deviates from the original railway, but is marked as railtrail */
      line/line-color: @offrailtrail;
      line/line-width: @offrailtrail-width;
    }
    [tracktype = 'grade3'], [tracktype = 'grade4'], [tracktype = 'grade5'], [surface = 'gravel'], [surface = 'rock'], [surface = 'sand'] {
      line/line-color: @railtrail-badtrack;
    }
    /*
    [zoom >= 14][railway = 'disused'] {
      line/line-color: @warning;
      line/line-dasharray: 1.0,3.0;
      ::inner {
        line/line-color: @railtrail;
        line/line-width: @railtrail-inner-width;
      }
    }
    */
  }
}

