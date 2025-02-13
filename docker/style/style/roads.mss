/* For the main linear features, such as roads and railways. */
@railtrail:rgba(60, 199, 187, 0.6);
@railtrail-width: 8;

#railtrails {
  [zoom >= 5] {
    line/line-color: @railtrail;
    line/line-join: round;
    line/line-cap: round;
    line/line-width: @railtrail-width;
  }
}

