(define (problem strips-gripper-x-2)
   (:domain gripper-strips)
   (:objects rooma roomb roomc ball3 ball2 ball1 ball4 ball5 left right rob)
   (:init (room rooma)
          (room roomb)
          (room roomc)

          (ball ball5)
          (ball ball4)
          (ball ball3)
          (ball ball2)
          (ball ball1)

          (robot rob)

          (at-robby rob rooma)

          (free left)
          (free right)

          (at ball5 roomc)
          (at ball4 roomc)
          (at ball3 roomb)
          (at ball2 rooma)
          (at ball1 rooma)

          (gripper left rob)
          (gripper right rob)
          )

   (:goal (and
               (at ball5 roomb)
               (at ball4 roomb)
               (at ball3 roomb)
               (at ball2 roomb)
               (at ball1 roomb))))