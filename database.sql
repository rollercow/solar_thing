create table solarGeneration (
	updateTime timestamp without time zone,
	voltPV1 NUMERIC(4,1),
	ampPV1 NUMERIC(3,1),
	wattPV1 smallint,
	voltPV2 NUMERIC(4,1),
	ampPV2 NUMERIC(3,1),
	wattPV2 smallint,
	voltAC NUMERIC(4,1),
	ampAC NUMERIC(3,1),
	wattAC smallint,
	wattExport smallint,
	dayYeild NUMERIC(3,1),
	totalYield NUMERIC(6,1),
	feedIn NUMERIC(6,1),
	consumed NUMERIC(6,1),
	status text
);