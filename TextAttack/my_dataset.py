import textattack
dataset = [("We enjoyed the movie a lot!", 1), 
           ("films adapted from comic books have had plenty of success , whether they're about superheroes ( batman , superman , spawn ) , or geared toward kids ( casper ) or the arthouse crowd ( ghost world ) , but there's never really been a comic book like from hell before . ", 1),
            ("for starters , it was created by alan moore ( and eddie campbell ) , who brought the medium to a whole new level in the mid '80s with a 12-part series called the watchmen .", 1 ),
            ("all of this , of course , leads up to the predictable climax . ", 1), 
            ("I do not watch this movie again. ",0),
            ("Never go see the terrible movie .",0),
            ("after the first fifteen minutes , it quickly becomes apparent that it is not . ", 0),
            ("the ghetto in question is , of course , whitechapel in 1888 london's east end . ", 1),
           ("Absolutely horrible film.", 0), 
           ("Our family had a fun time!", 1),
           ("avoid this film at all costs ." ,0),
           ("problems are solved when the obstacle is removed . " ,0),
           ("it's the cinematic equivalent to a good read , novelistic in its approach with themes rarely found in american movies . " ,1),
           ("every now and again it's fun to watch a really bad movie . " , 1)
           ]
dataset = textattack.datasets.Dataset(dataset)
