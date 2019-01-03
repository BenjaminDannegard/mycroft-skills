# TODO: Add an appropriate license to your skill before publishing.  See
# the LICENSE file for more information.

# Below is the list of outside modules you'll be using in your skill.
# They might be built-in to Python, from mycroft-core or from external
# libraries.  If you use an external library, be sure to include it
# in the requirements.txt file so the library is installed properly
# when the skill gets installed later by a user.

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.skills.context import adds_context, removes_context
from mycroft.skills.core import FallbackSkill
from mycroft.util.log import LOG
from mycroft.util import play_wav as play
from time import sleep
import os
import sys

skill_path = "/opt/mycroft/skills/skill-darth-plagueis/"
sys.path.append(skill_path)
import led # for led control on the aiy voice kit
int counter = 0;

# This was my first test based on the default skill template
# See the 2nd class below for more sophisticated dialog control
# ToDo: delete
class WalkSkillBasic(MycroftSkill):

    # The constructor of the skill, which calls MycroftSkill's constructor
    def __init__(self):
        super(WalkSkillBasic, self).__init__(name="WalkSkill")

        self.finished = False

    # The "handle_xxxx_intent" function is triggered by Mycroft when the
    # skill's intent is matched.  The intent is defined by the IntentBuilder()
    # pieces, and is triggered when the user's utterance matches the pattern
    # defined by the keywords.  In this case, the match occurs when one word
    # is found from each of thewhat files:
    #    vocab/en-us/Hello.voc
    #    vocab/en-us/World.voc
    # In this example that means it would match on utterances like:
    #   'Hello world'
    #   'Howdy you great big world'
    #   'Greetings planet earth'
    @intent_handler(IntentBuilder("").require("Darth_Plagueis"))
    def handle_darth_plagueis_intent(self, message):
        # In this case, respond by simply speaking a canned response.
        # Mycroft will randomly speak one of the lines from the file
        #    dialogs/en-us/hello.world.dialog

        def no_response():
            self.speak_dialog("tragedy5")
            finished = True
            return

        choice = self.get_response('tragedy1')
        if not choice:
            no_response()
        else:
            choice = self.get_response('tragedy2')
            if not choice:
                no_response()
            else:
                choice = self.get_response('tragedy3')
                if not choice:
                    no_response()
                else:
                    choice = self.get_response('tragedy4')
                    if not choice:
                        no_response()
                    else:
                        self.speak_dialog("tragedy5")


        self.finished = True

    # look at converse



# The "stop" method defines what Mycroft does when told to stop during
    # the skill's execution. In this case, since the skill's functionality
    # is extremely simple, there is no need to override it.  If you DO
    # need to implement stop, you should return True to indicate you handled
    # it.
    #
    def stop(self):
        return True


class WalkSkillContext(MycroftSkill):
    def __init__(self, mode='tts'):
        super(WalkSkillContext, self).__init__(name='WalkSkill')
        self.darkside = False
        self.started = False
        if mode=='wav':
            self.wav_mode = True
        else:
            self.wav_mode = False

        LOG("WalkSkill").debug("Walking skill loaded")


    @intent_handler(IntentBuilder('Walk').require('Darth_Plagueis'))
    @adds_context('WalkContext')
    def handle_darth_plagueis_intent(self, message):
        self.started = True

        self.speak("It is raining cats and dogs!")

        # ToDo: find a better way to move to the next line if there is no response
        # the blank dialog below does not work with the Google TTS, so removed
        # '''
        # response = self.get_response('blank')

        # if response == "yes" or response == "yeah":
        #     self.speak("Not from a Jedi")
        #     self.remove_context('PlagueisContext')
        # else:
        #     self.story()
        # '''


    @intent_handler(IntentBuilder('WalkOpportunity').require('save_death').require('PlagueisContext').build())
    @adds_context('SaveFromDeathContext')
    def handle_save_from_death_intent(self, message):

        if(counter == 0){
        self.speak("Yes! Now is a good time, but it is cold outside, bring me a sweater", expect_response=False)
        counter = 1;}
        else if(counter == 1){
        self.speak("No! We went for a walk recently.", expect_response=False)
        counter = 0;}   
        }


    @intent_handler(IntentBuilder('WhatHappened').require('happened').require('PlagueisContext').build())
    @adds_context('SaveFromDeathContext')
    def what_happened_intent(self, message):
            self.speak("")

    @intent_handler(IntentBuilder('LearnThisPower').require('learn')
                    .require('SaveFromDeathContext').require('PlagueisContext').build())
    @removes_context('PlagueisContext')
    @removes_context('SaveFromDeathContext')
    def handle_can_be_learned_intent(self, message):
        if self.wav_mode:
            play(os.path.join(skill_path,'audio/tragedy of darth plagueis 5.wav'))
            led.wait(1, led.LED.ON)
        else:
            self.speak("Not from a Jedi")


    @removes_context('PlagueisContext')
    @removes_context('SaveFromDeathContext')
    def stop(self):
        if self.started and not self.darkside:
                if self.wav_mode:
                    play(os.path.join(skill_path,'audio/tragedy of darth plagueis 3.wav'))
                    led.wait(8)

                else:
                    self.speak("The dark side of the Force is a pathway to many abilities some consider to be unnatural.")

        return True


def create_skill():
    return PlagueisSkillContext(mode='wav')
