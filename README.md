# WhistleCode
Ever wanted to code entirely hands free? Well now you can using Whistle Code!
Just start it up, whisle a high note, then a low note, then whistle away to program whatever you want!
The system works based off of morse code but with high and low whistles rather than dots and dashes.
It takes a bit of practice to get used to but it works.
You simply whistle the code for a letter with little spaces between the code-points, then wait until the character is recognised to start the next letter.
You can play with the parameters if you get really good and want to go faster than the default quantization.
I have basically only implemented the charactors needed for the demo but it should be easy to add more or change exsiting ones in the `morse.py` file.
It is possible to use other sound sources like singing or an instrement but I have only done limited testing and it does not seem to work super well.
The closer the sound is to a sine wave, the better it will work I suspect.
No, I did not write this readme using Whistle Code.

## There are a few special charactors implemented
* Error is backspace
* Wait is space
* Shift to Wabun code is caps lock
