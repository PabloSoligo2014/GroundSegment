select *
from groundSegment_tle
where groundSegment_tle.satellite_id=3

delete from groundSegment_propagationdetail;
delete from groundSegment_propagation;

select groundSegment_propagationdetail.dt, groundSegment_propagationdetail.earthDistance
from groundSegment_propagationdetail inner join groundSegment_propagation on groundSegment_propagation.id=groundSegment_propagationdetail.propagation_id
where groundSegment_propagation.satellite_id=3 and groundSegment_propagationdetail.earthDistance<>0





