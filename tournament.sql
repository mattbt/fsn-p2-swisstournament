-- Table definitions for the tournament project.

CREATE TABLE tournament (
	id						SERIAL PRIMARY KEY,
	name					VARCHAR(50)
);

CREATE TABLE player (
	id						SERIAL PRIMARY KEY,
	username				varchar(40) NOT NULL,
	currentTournament		INTEGER REFERENCES tournament(id)
);

-- possible results: WIN1, WIN2, BYE, DRAW
CREATE TABLE match_result (
	id						INTEGER PRIMARY KEY,
	description				VARCHAR(100) NOT NULL
);
INSERT INTO match_result VALUES (1, 'WIN1');
INSERT INTO match_result VALUES (2, 'WIN2');
INSERT INTO match_result VALUES (3, 'BYE');
INSERT INTO match_result VALUES (4, 'DRAW');

CREATE TABLE single_match (
	id						SERIAL PRIMARY KEY,
	id_tournament			INTEGER REFERENCES tournament(id),
	id_player1				INTEGER REFERENCES player(id) NOT NULL,
	id_player2				INTEGER REFERENCES player(id),
	mresult					INTEGER REFERENCES match_result(id),
	-- if BYE, check id_player2 to be NULL > tested
	CHECK ((mresult = 3 AND id_player2 IS NULL OR mresult <> 3 AND id_player2 IS NOT NULL)
			AND (id_player1 < id_player2))
);
-- Limit BYE to one per tournament-player
CREATE UNIQUE INDEX one_bye_per_tournament_player ON single_match (id_tournament, id_player1)
    WHERE mresult = 3;

	

-- VIEWS	
CREATE VIEW player_total_matches AS
	SELECT p.id, p.username, p.currentTournament, COUNT(s.id) AS total_matches
	FROM player p
	LEFT JOIN single_match s ON (p.id=s.id_player1) OR (p.id=s.id_player2)
	GROUP BY p.id
	ORDER BY total_matches DESC;

-- a bye counts as a free win 
CREATE VIEW player_total_win AS
	SELECT p.id, p.username, p.currentTournament, COUNT(s.id) AS total_win
	FROM player p
	LEFT JOIN single_match s ON (p.id=s.id_player1 AND s.mresult = 1) OR (p.id=s.id_player2 AND s.mresult = 2) OR (p.id=s.id_player1 AND s.mresult = 3)
	GROUP BY p.id
	ORDER BY total_win DESC;

CREATE VIEW player_byes AS
	SELECT 	p.id, 
			p.currentTournament, 
			COUNT(s.id) AS bye
	FROM player p
	LEFT JOIN single_match s ON (p.id=s.id_player1)
	WHERE s.mresult = 3
	GROUP BY p.id
	ORDER BY bye DESC;
	
-- Sum of already-played-against opponents'wins
CREATE VIEW player_total_OMW AS
	SELECT 	t1.id, 
			t1.username, 
			CASE WHEN SUM(t1.total_win) IS NULL THEN 0 ELSE SUM(t1.total_win) END AS omw
	FROM
		(SELECT DISTINCT    p.id, 
							p.username,
							CASE 	WHEN p.id=s.id_player1  THEN s.id_player2
									WHEN p.id=s.id_player2  THEN s.id_player1
							END AS opposite,
							tw.total_win AS total_win
		FROM player p
		LEFT JOIN single_match s ON (p.id=s.id_player1) OR (p.id=s.id_player2)
		LEFT JOIN player_total_win tw 
			ON 	CASE 	WHEN p.id=s.id_player1  THEN tw.id=s.id_player2
						WHEN p.id=s.id_player2  THEN tw.id=s.id_player1
				END
		) AS t1
	GROUP BY t1.id, t1.username
	ORDER BY omw DESC;

-- aggregate the 4 above views
CREATE VIEW player_standings AS
	SELECT 	tm.id, 
			tm.username, 
			tm.currentTournament, 
			w.total_win, 
			omw.omw, 
			tm.total_matches, 
			CASE WHEN pb.bye IS NULL THEN 0 ELSE pb.bye END AS bye
	FROM player_total_matches tm
	LEFT JOIN player_total_win w ON tm.id = w.id
	LEFT JOIN player_total_OMW omw on tm.id = omw.id
	LEFT JOIN player_byes pb on tm.id = pb.id
	ORDER BY tm.currentTournament DESC, w.total_win DESC, omw.omw DESC;
	
	

