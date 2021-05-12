# Submit Assignment 2:

  ## Manual: <br />
  ### Syntax: <br />

    $ python3 augmentation \images_directory \method --sample \sample --probability \probability --first \parameter_1 --second \parameter_2

  ### Example: <br />

    $ python3 augmentation images rotate --sample 10 -p 0.9 -f 10 -s 10
    $ python3 augmentation images zoom -f 1.1 -s 1.5
    $ python3 augmentation images crop_random -S 10 -f 0.8

  ### Test: Use `--test` or `-t` to see an example

    $ python3 augmentation.py images/ crop_random -f 0.8 --test
    $ python3 augmentation.py images/ flip_left_right -t

  ### Help: Use `-h` or `--help` to get more information.<br />

    $ python3 augmentation -h
    $ python3 augmentation --help

   ### Remark: <br />
   - `images_directory` : source directory
   - `method` : {rotate,zoom,flip_left_right,flip_top_bottom,zoom_random,crop_random}
   - `sample` : number of images (`sample` = 0: all images) default by 0
   - `probabilty` : default by 0.6
   - `parameter_1` : zoom : min factor | rotate : max left rotation | zoom_random : percentage area | crop_random : percentage area
   - `parameter_2` : zoom : max factor | rotate : max right rotation

 
  ## Results: <br />
   >![system schema](/img.png)
