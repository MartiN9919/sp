# https://dev.mysql.com/doc/mysql-partitioning-excerpt/5.6/en/partitioning-management-range-list.html

ALTER TABLE geo
PARTITION BY RANGE COLUMNS (part)(
    PARTITION p001 VALUES LESS THAN (2),
    PARTITION p002 VALUES LESS THAN (3),
    PARTITION p003 VALUES LESS THAN (4),
    PARTITION p999 VALUES LESS THAN (MAXVALUE)
);

#REORGANIZE PARTITION p999 INTO (
#    PARTITION p004 VALUES LESS THAN (4),
#    PARTITION p999 VALUES LESS THAN (MAXVALUE)
#);

#DROP PARTITION p001;




SELECT
  vec_data.geo_node.id,
  vec_data.geo_node.address,
  ST_AsGeoJSON(PointFromText(CONCAT('POINT(',vec_data.geo_node.lon,' ',vec_data.geo_node.lat,')'),1)) AS location
FROM vec_data.geo_prop
  INNER JOIN vec_data.rel__geo_node__geo_prop
  ON vec_data.geo_prop.id=vec_data.rel__geo_node__geo_prop.geo_prop_id
  INNER JOIN vec_data.geo_node
  ON vec_data.geo_node.id=vec_data.rel__geo_node__geo_prop.geo_node_id
WHERE vec_data.geo_prop.id=1



update geo_node set location = PointFromText(CONCAT('POINT(',`lon`,' ',`lat`,')'),1)






#SET @tt = POINT(55.5212, 27.7288);
#SELECT ST_SRID(@tt);

#SET @tt = ST_GeomFromText("POINT(26.83553 55.28771)", 4326);
#SELECT name, ST_AsText(location),ST_AsText(@tt), ST_SRID(location), ST_SRID(@tt)  FROM geo_geometry
#WHERE ST_Contains(location, @tt);

SET @tt = ST_GeomFromText("POINT(25.50695 52.93449)", 4326);
SELECT name, ST_AsText(location),ST_AsText(@tt), ST_SRID(location), ST_SRID(@tt)  FROM geo_geometry
WHERE ST_Contains(location, @tt);





Вариант 1
INSERT IGNORE INTO obj_geometry_col SET id=1, category='tests', name='test_geo', location=ST_GeomFromGeoJson('
{
   "type": "GeometryCollection",
   "geometries": [{"type": "Polygon", "coordinates": [[[36.475, 59.624], [42.535, 58.217], [45.175, 61.48], [36.475, 59.624]]]}]
}')

Вариант 2
INSERT IGNORE INTO obj_geometry_col SET id=1, category='tests', name='test_geo', location=ST_GeomFromGeoJson('
            {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {},
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [ [
                            [36.475, 59.624],
                            [42.535, 58.217],
                            [45.175, 61.480],
                            [36.475, 59.624]
                        ] ]
                    }
                }
            ]}
        ')
