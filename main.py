#Console Based Blackjack Free Bet
#Rules:
#  8 Decks of Cards
#  Dealer always stands on 17
#  Double Available after any two initial cards
#  Free spli on all pairs except 10, J, Q, K
#  Free double on your two-card hard 9, 10, and 11 totals
#  Split initial cards of equal value
#  One split per hand
#  Single card dealt to each split Aces
#  No double after split
#  Six Card Charlie: you win if you have six cards with a value of 21 or less
#  Insurance offered when the dealer shows an Ace
#  Blackjack pays 3 to 2 and beats score of 21
#  Insurance pays 2 to 1
#  Your bet is returned when hands are of equal value
#  Your bet is returned when the dealer busts with a score of 22.
#
#  Card Format:
#  Suites: Spades (S), Hearts (H), Diamonds (D), Clubs (C)
#  Values: 2, 3, 4, 5, 6, 7, 8, 9, 10 (0),Jack (J), Queen (Q), King (K), Ace, (A)
#
#

# Imports
import os
from random import shuffle



# Global Variables
ProgramActive = True
DeckTemplate = ['S2','S3','S4','S5','S6','S7','S8','S9','S0','SJ','SQ','SK','SA',
                'H2','H3','H4','H5','H6','H7','H8','H9','H0','HJ','HQ','HK','HA',
                'D2','D3','D4','D5','D6','D7','D8','D9','D0','DJ','DQ','DK','DA',
                'C2','C3','C4','C5','C6','C7','C8','C9','C0','CJ','CQ','CK','CA']
NumberOfDecks = 8
DoubleSpace = '  '

# Dynamic Variables
MenuActive = True
GameActive = False
DealersDeck = []
DealerScoreSoft = DealerScoreHard = 0
DealerHand = []
PlayerScoreSoft = PlayerScoreHard = 0
PlayerHand = []
PlayerCash = 100 # Default cash for player is $100

# Functions
def clear():
  os.system('cls' if os.name=='nt' else 'clear')

def CardDecoder(card: str, currentSoftScore: int,):  # Decode the Card Lingo used in this program
  suite = ''
  value = softValue = hardValue = 0
  
  match card[0]: # Suite
    case 'S':
      suite = 'S'
      print('The Suite is a Spade')
    case 'H':
      suite = 'H'
      print('The Suite is a Heart')
    case 'D':
      suite = 'D'
      print('The Suite is a Diamond')
    case 'C':
      suite = 'C'
      print('The Suite is a Club')

  match card[1]: # Value
    case '2':
      softValue = hardValue = 2
    case '3':
      softValue = hardValue = 3
    case '4':
      softValue = hardValue = 4
    case '5':
      softValue = hardValue = 5
    case '6':
      softValue = hardValue = 6
    case '7':
      softValue = hardValue = 7
    case '8':
      softValue = hardValue = 8
    case '9':
      softValue = hardValue = 9
    case '0': # 10
      softValue = hardValue = 10
    case 'J': # Jack
      softValue = hardValue = 10
    case 'Q': # Queen
      softValue = hardValue = 10
    case 'K': # King
      softValue = hardValue = 10
    case 'A': # Ace
      # Needs more work for Soft and Hard Hands
      softValue = 1
      # value = 11 if not currentScore + 11 > 21 else 1
      
  return (suite, softValue, hardValue)

def DealerDeckShuffle():
# Call this function whenever the Dealers Deck needs to be replaced.
  if DealersDeck != 0:
    # Clear the Dealers Deck if it is not currently empty
    DealersDeck.clear()
  
  for x in range(NumberOfDecks):
    # Amount of decks added is determined by the NumberOfDecks Variable
    for card in DeckTemplate:
      # Add one of each card in the template to the Dealers Deck
      DealersDeck.append(card)
  shuffle(DealersDeck)

def CalculateScore(hand: list[str]):
  softScore = 0 # Return Value
  hardScore = 0
  for card in hand:
    softScore += CardDecoder(card, score)[1]
    hardScore += CardDecoder(card, score)[2]
  return (softScore, hardScore)

def DealCard():
  card = DealersDeck[0]
  del DealersDeck[0]
  return card

def ClearHands():
  PlayerHand.clear()
  DealerHand.clear()
  
def Opening():
  # Deal the Starting hand
  # Player, Dealer, Player, Dealer face down
  PlayerHand.append(DealCard())
  PlayerHand.append(DealCard())
  DealerHand.append(DealCard())
  DealerHand.append(DealCard())
  pass

def display(): # Output what the player needs to see
  clear()
  print(f'=------------------=')
  print(f'| {DealerHand[0]}               |')
  print(f'|                  |')
  print(f'|                  |')
  print(f'|                  |')
  print(f'|                  |')
  print(f'|                  |')
  print(f'|                  |')
  print(f'|                  |')
  print(f'|                  |')
  print(f'|                  |')
  print(f'| {len(PlayerHand)}               |')
  print(f'|     {PlayerHand[5] if len(PlayerHand) > 5 else DoubleSpace}           |')
  print(f'|    {PlayerHand[4] if len(PlayerHand) > 4 else DoubleSpace}            |')
  print(f'|   {PlayerHand[3] if len(PlayerHand) > 3 else DoubleSpace}             |')
  print(f'|  {PlayerHand[2] if len(PlayerHand) > 2 else DoubleSpace}              |')
  print(f'| {PlayerHand[1]}       SOFT: {PlayerScoreSoft} |')
  print(f'|{PlayerHand[0]}        Hard: {PlayerScoreHard} |')
  print(f'=------------------=')
  pass

def playBlackjack():
  # Game Logic
  # Make Deck
  DealerDeckShuffle()
  Opening()

  while(GameActive):
    CalculateScore(PlayerHand)
    display()
    input()
    if len(PlayerHand) < 6:
      PlayerHand.append(DealCard())
      pass

    
    pass
  pass



# Main Code
while(ProgramActive):

  # Main Menu
  while(MenuActive):
    clear()
    print("Welcome to BlackJack")
    print("1 | Play")
    print("2 | Settings")
    print("3 | Quit")
    userSelection = input("Choose a menu option: ")
    #print (userSelection)
    match userSelection:
      case '1':
        GameActive = True
        playBlackjack()
      case '2':
        print()
      case '3':
        MenuActive = False
        ProgramActive = False
        print('Thanks for playing!')
      case _:
        print("Please enter a valid input.")