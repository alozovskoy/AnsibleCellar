BEGIN TRANSACTION;
CREATE TABLE "tasks" (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`rc`	INTEGER,
	`start`	INTEGER,
	`stop`	INTEGER,
	`logname`	TEXT,
	`ppid`	INTEGER,
	`playbook`	TEXT,
	`inventory`	TEXT,
	`vars`	TEXT,
	`type`	INTEGER,
	`owner`	TEXT,
	`status`	TEXT,
	`tags`	TEXT,
	`skipped_tags`	TEXT
);
CREATE TABLE "steps" (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`taskid`	INTEGER NOT NULL,
	`stepNumber`	INTEGER NOT NULL,
	`stepName`	TEXT,
	`start`	INTEGER,
	`stop`	INTEGER,
	`hostname`	TEXT,
	`data`	INTEGER,
	`status`	TEXT
);
COMMIT;
