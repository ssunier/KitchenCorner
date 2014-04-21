drop table if exists recipequantity;
drop table if exists fridgequantity;
drop table if exists ingredient;
drop table if exists fridge;
drop table if exists recipe;
drop table if exists users;

create table recipe (
       rid int auto_increment not null primary key,
       title varchar(50),
       totaltime integer,
       image varchar(200), 
       addedby varchar(50),
       instructions varchar(500)
       ) 
       ENGINE = InnoDB;

INSERT into recipe VALUES (0, 'Italian Pasta Salad',20,null,1,
       	    	   	      'In large bowl, toss all ingredients together. Add dressing last and mix well.'),
			  (0, 'Pumpkin Pudding',10,null,2,
			      '1. In a bowl, combine pumpkin, molasses and spices. Gradually add milk. 
			      Add pudding mix; beat slowly with an electric mixer until thick, about 1 minute. 
			      Fold in whipped cream.
			      2. Pour into a serving bowl or individual serving dishes. 
			      Chill for 1 hour. 
			      If desired, top each serving with a dollop of whipped cream and a sprinkle of cinnamon.');


create table users (
       uid int auto_increment not null primary key,
       username varchar(50),
       password varchar(50),
       name varchar(50)
       )
       ENGINE = InnoDB;

INSERT into users VALUES (1, 'skim22', 'abc', 'Soojin'),
       	    	  	 (2, 'ssunier','random', 'Sheridan'),
			 (0, 'test','lalala','TestUser');

create table fridge (
       fid int auto_increment not null primary key,
       uid int not null,
       foreign key (uid) references users(uid) on delete restrict
       )
       ENGINE = InnoDB;

INSERT into fridge VALUES (1, 1),
       	    	   	  (2, 2),
			  (3, 3);

create table ingredient (
      id int auto_increment not null primary key,
      name varchar(50),
      unit varchar(10)
      )
      ENGINE = InnoDB;

INSERT into ingredient VALUES (1, 'flour', 'cup'),
       	    	       	      (2, 'cheese', 'cup'),
			      (3, 'broccoli', 'head'),
			      (4, 'garlic', 'clove'),
			      (5, 'chicken', 'lb'),
			      (6, 'rotini', 'lb'),
			      (7, 'pepperoni','cup'),
			      (8, 'black olives', 'cup'),
			      (9, 'italian dressing', 'bottle'),
			      (10, 'vanilla yogurt','oz'),
			      (11, 'pumpkin','cup'),
			      (12,'ground nutmeg','tsp'),
			      (13, 'ground cinnamon','tsp');

create table fridgequantity (
       fid int not null,
       id int not null,
       quantity decimal(4,2),
       foreign key (fid) references fridge(fid) on delete restrict,
       foreign key (id) references ingredient(id) on delete restrict
       )
       ENGINE = InnoDB;

INSERT into fridgequantity VALUES (1, 1, 5),
       	    		   	  (2, 2, 1),
				  (3, 3, 7);


create table recipequantity (
       rid int not null,
       id int not null,
       quantity decimal(4,2),
       foreign key (rid) references recipe(rid) on delete restrict,
       foreign key (id) references ingredient(id) on delete restrict
       )
       ENGINE = InnoDB;
