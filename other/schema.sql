CREATE TABLE Profil(
   profil_id INT AUTO_INCREMENT,
   bio TEXT,
   profile_picture VARCHAR(255) ,
   cover_picture VARCHAR(255) ,
   last_active DATETIME DEFAULT CURRENT_TIMESTAMP,
   PRIMARY KEY(profil_id)
);

CREATE TABLE Skill(
   skill_id INT AUTO_INCREMENT,
   name VARCHAR(100)  NOT NULL,
   PRIMARY KEY(skill_id),
   UNIQUE(name)
);

CREATE TABLE Experience(
   experience_id INT AUTO_INCREMENT,
   company VARCHAR(200)  NOT NULL,
   position_ VARCHAR(200)  NOT NULL,
   description TEXT,
   start_date DATE NOT NULL,
   end_date DATE,
   is_current BOOLEAN DEFAULT FALSE,
   profil_id INT NOT NULL,
   PRIMARY KEY(experience_id),
   FOREIGN KEY(profil_id) REFERENCES Profil(profil_id)
);

CREATE TABLE Post(
   post_id INT AUTO_INCREMENT,
   content TEXT NOT NULL,
   image VARCHAR(255) ,
   created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
   profil_id INT NOT NULL,
   PRIMARY KEY(post_id),
   FOREIGN KEY(profil_id) REFERENCES Profil(profil_id)
);

CREATE TABLE Comment(
   comment_id INT AUTO_INCREMENT,
   content TEXT NOT NULL,
   created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
   post_id INT NOT NULL,
   profil_id INT NOT NULL,
   PRIMARY KEY(comment_id),
   FOREIGN KEY(post_id) REFERENCES Post(post_id),
   FOREIGN KEY(profil_id) REFERENCES Profil(profil_id)
);

CREATE TABLE Trophy(
   trophy_id INT AUTO_INCREMENT,
   name VARCHAR(100)  NOT NULL,
   description TEXT,
   required_likes INT NOT NULL,
   PRIMARY KEY(trophy_id)
);

CREATE TABLE Notification(
   notification_id INT AUTO_INCREMENT,
   notification_type VARCHAR(50)  NOT NULL,
   message TEXT NOT NULL,
   is_read BOOLEAN DEFAULT FALSE,
   created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
   comment_id INT,
   post_id INT,
   to_user_id INT NOT NULL,
   from_user_id INT NOT NULL,
   PRIMARY KEY(notification_id),
   FOREIGN KEY(comment_id) REFERENCES Comment(comment_id),
   FOREIGN KEY(post_id) REFERENCES Post(post_id),
   FOREIGN KEY(to_user_id) REFERENCES Profil(profil_id),
   FOREIGN KEY(from_user_id) REFERENCES Profil(profil_id)
);

CREATE TABLE auth_user(
   auth_user_id INT AUTO_INCREMENT,
   username VARCHAR(50) ,
   email VARCHAR(50) ,
   password VARCHAR(50) ,
   first_name VARCHAR(50) ,
   last_name VARCHAR(50) ,
   is_active BOOLEAN,
   is_staff BOOLEAN,
   is_superuser BOOLEAN,
   profil_id INT NOT NULL,
   PRIMARY KEY(auth_user_id),
   UNIQUE(profil_id),
   FOREIGN KEY(profil_id) REFERENCES Profil(profil_id)
);

CREATE TABLE UserSkill(
   profil_id INT,
   skill_id INT,
   level TEXT DEFAULT 'BEGINNER',
   PRIMARY KEY(profil_id, skill_id),
   FOREIGN KEY(profil_id) REFERENCES Profil(profil_id),
   FOREIGN KEY(skill_id) REFERENCES Skill(skill_id)
);

CREATE TABLE Connection(
   from_user_id INT,
   to_user_id INT,
   status VARCHAR(50)  DEFAULT 'PENDING',
   created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
   PRIMARY KEY(from_user_id, to_user_id),
   FOREIGN KEY(from_user_id) REFERENCES Profil(profil_id),
   FOREIGN KEY(to_user_id) REFERENCES Profil(profil_id)
);

CREATE TABLE Reaction(
   profil_id INT,
   post_id INT,
   reaction_type VARCHAR(50)  NOT NULL,
   created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
   PRIMARY KEY(profil_id, post_id),
   FOREIGN KEY(profil_id) REFERENCES Profil(profil_id),
   FOREIGN KEY(post_id) REFERENCES Post(post_id)
);

CREATE TABLE UserTrophy(
   profil_id INT,
   trophy_id INT,
   earned_at DATETIME DEFAULT CURRENT_TIMESTAMP,
   PRIMARY KEY(profil_id, trophy_id),
   FOREIGN KEY(profil_id) REFERENCES Profil(profil_id),
   FOREIGN KEY(trophy_id) REFERENCES Trophy(trophy_id)
);
