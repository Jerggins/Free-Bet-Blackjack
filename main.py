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
actionCases = []
DealersDeck = []
dealerReveal = False
DealerScore = 0
DealerHand = []
playerTurn = True
PlayerScoreSoft = PlayerScoreHard = 0
PlayerHand = []
PlayerCash = 25 # Default cash for player is $100
PlayerWager = 0
playerInsuranceWager = 0
odds = [2.5,2]

  # Action Condition Variables
splitAction = False

# Functions
def clear():
  os.system('cls' if os.name=='nt' else 'clear')
  
def CardDecoder(card: str):
  # Decode the Card Lingo used in this program
  suite = ''
  softValue = hardValue = 0
  
  match card[0]: # Suite
    case 'S':
      suite = 'S'
    case 'H':
      suite = 'H'
    case 'D':
      suite = 'D'
    case 'C':
      suite = 'C'

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
      hardValue = 11
      # value = 11 if not currentScore + 11 > 21 else 1
      
  return (suite, softValue, hardValue)

def DealerDeckShuffle():
# Call this function whenever the Dealers Deck needs to be replaced.
  if len(DealersDeck) != 0:
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
    softScore += CardDecoder(card)[1]
    hardScore += CardDecoder(card)[2]
  # If the Hard Score is over 21, but the Soft Score is still under 21
  if(hardScore > 21 and softScore <= 21):
    # Force the Player to use their softscore
    hardScore = softScore
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
  print(f' {DealerHand[0]}            {CalculateScore(DealerHand)[1] if dealerReveal is True else CardDecoder(DealerHand[0])[2]}')
  print(f'  {DealerHand[1] if dealerReveal is True else "**"}')
  print(f'   {DealerHand[2] if len(DealerHand) > 2 else DoubleSpace}')
  print(f'    {DealerHand[3] if len(DealerHand)  > 3 else DoubleSpace}')
  print(f'     {DealerHand[4] if len(DealerHand)  > 4 else DoubleSpace}')
  print(f'      {DealerHand[5] if len(DealerHand)  > 5 else DoubleSpace}')
  print(f'')
  print(f'')
  print(f'')
  print(f'')
  print(f'')
  print(f'     {PlayerHand[5] if len(PlayerHand) > 5 else DoubleSpace}')
  print(f'    {PlayerHand[4] if len(PlayerHand) > 4 else DoubleSpace}')
  print(f'   {PlayerHand[3] if len(PlayerHand) > 3 else DoubleSpace}')
  print(f'  {PlayerHand[2] if len(PlayerHand) > 2 else DoubleSpace}     Wager: ${PlayerWager}')
  print(f' {PlayerHand[1]}       SOFT:  {CalculateScore(PlayerHand)[0]}')
  print(f'{PlayerHand[0]}        Hard:  {CalculateScore(PlayerHand)[1]}')
  print(f'=------------------=')
  print(f'${PlayerCash}')
  pass

def ResetGame():
  global PlayerWager, dealerReveal, playerTurn, playerInsuranceWager
  playerInsuranceWager = 0
  PlayerWager = 0
  playerTurn = True
  dealerReveal = False
  ClearHands()
  
  pass

def PlaceBets():
  global PlayerWager, PlayerCash
  
  while PlayerWager == 0:
    
    try:
      PlayerWager = float(input(f'Please make a wager. Money Available (${PlayerCash}) : '))
      if PlayerWager > PlayerCash or PlayerWager < 1:
        print(f'\nInsufficient Funds, please enter a amount between 1 and {PlayerCash}')
        PlayerWager = 0
    except:
      print('\nPlease enter a valid amount.')
      PlayerWager = 0
  
  PlayerCash -= PlayerWager
  pass

def Blackjack(hand: list[str]):
  return CalculateScore(hand)[1] == 21 and len(hand) == 2
    
def Payout(wager, victoryType: int):
  global PlayerCash
  payout = 0
  match victoryType:
    case 0: # Blackjack
      payout = wager * odds[0]
      PlayerCash += payout
      print(f'Winnings: ${payout}')
    case 1: # Standard Win
      payout = wager * odds[1]
      PlayerCash += payout
      print(f'Winnings: ${payout}')
    case 2: # Insurance Payout
      payout = wager * odds[1]
      PlayerCash += payout
      print(f'Winnings: ${payout}')
    case 3: # Push
      payout = wager
      PlayerCash += payout
      print(f'Winnings: ${payout}')
def DealerBlackjackCheck():
  return CalculateScore(DealerHand)[1] == 21
    
# Action Conditions
def updateCases(playerAction: str):
  global actionCases 
  actionCases = [
    playerAction == '',
    playerAction.lower() != 'h', # Hit
    playerAction.lower() != 's', # Stand
    playerAction.lower() != 'p', # Split
    playerAction.lower() != 'd'   # Double Down
  ]

# Split Check
def SplitCheck(hand: list[str]):
  
  # Eligible for split?
  if splitAction: # If user has already split their hands
    return False
  
  pass

# Insurance Check
def InsuranceCheck():
  global playerTurn, PlayerCash, playerInsuranceWager
  # If the Dealers first card is an Ace, offer insurance
  while True:
    if DealerHand[0][1] == 'A':
      if (PlayerWager / 2) > PlayerCash:
        print('You cannot afford insurance.')
        break
      else:
        print(f'Would you like Insurance? ({PlayerWager / 2})')
      # Loop until a valid answer is received
      prompt = input('Y/N: ')
      # If the user inputs a valid answer, break loop and continue
      if prompt.lower() == 'y':
        # If the User accepts Insurance, add half of their original wager to the wager
        PlayerCash -= (PlayerWager / 2)# Remove from Cash
        playerInsuranceWager += (PlayerWager / 2)# Add to wager
        # After insurance is collected, check if the Dealer has 21
        # If dealer does not have 21, continue as normal; Else, end the game and payout insurance
        break
      elif prompt.lower() == 'n': # No Insurance
        print('No insurance issued.')
        break
      else:
        print('Please input a valid option')
    else:
      break
  # Check if Dealer has blackjack
  if DealerBlackjackCheck(): # Check Dealers hand for Blackjack, If Blackjack...
    playerTurn = False  # End Turn
    print(f'Dealer shows a {DealerHand[0]} and {DealerHand[1]} for Blackjack')
    if playerInsuranceWager > 0: # If the player bought insurance
      Payout(playerInsuranceWager,2) # Payout insurance wager
  
# Double Down Check
def DoubleDownCheck(hand: list[str]):
  # No Double Down on Split Hands
  if splitAction:
    return False
  # Player may only have two cards to be eligible for Double Down
  # Free Double if two-card hard score is 9, 10, or 11
  return len(hand) == 2
def PlayerTurn():# The Player should be given a valid option for their turn
  global playerTurn, PlayerCash, PlayerWager
  prompt = '(H)it | (S)tand'
  playerAction = ''
  # Insurance Check
  if playerInsuranceWager == 0:
    InsuranceCheck()
  # Double Down Check
  if DoubleDownCheck(PlayerHand) and PlayerWager < PlayerCash:
    prompt += ' | (D)ouble Down'
  updateCases(playerAction)
  if Blackjack(PlayerHand):
    playerTurn = False      
  if playerTurn is True and any([CalculateScore(PlayerHand)[0] < 21, CalculateScore(PlayerHand)[1] < 21]) and len(PlayerHand) < 6:
    
    print(prompt)
    while all(actionCases):
      playerAction = input('Action: ')
      updateCases(playerAction)
    # Ensure Valid Selection
    match playerAction.lower():
      case 'h':
        PlayerHand.append(DealCard()) # Deal Card
      case 's':
        playerTurn = False # End Turn
      case 'd':
        
        # If Double Down is chosen, Double the Wager and make the next card the final card
        PlayerCash -= PlayerWager # Remove funds
        PlayerWager += PlayerWager # Double Down
        PlayerHand.append(DealCard()) # Deal Card
        playerTurn = False # End Turn
      case 'l':
        pass
  else:
    playerTurn = False
def DetermineResults():
  playerScores = CalculateScore(PlayerHand)
  dealerScores = CalculateScore(DealerHand)
  #1: If player is over 21 they bust
  if playerScores[0] > 21 and playerScores[1] > 21:
    return 0 
  #2: If dealer is 22, Push
  elif any([dealerScores[0] == 22, dealerScores[1] == 22]):
    return 1
  #3: If dealer is over 22 and player is under 22, payout
  elif any([dealerScores[0] > 22, dealerScores[1] > 22]):
    return 2
  #4: Dealer and Player are tied
  elif dealerScores[1] == playerScores[1]:
    return 3
  #5: Dealer's score is higher
  elif dealerScores[1] > playerScores[1]:
    return 4
  #6: Player's score is higher
  elif dealerScores[1] < playerScores[1]:
    return 5
def DealerTurn():
  global playerTurn, dealerReveal
  if not playerTurn:
    dealerReveal = True
    while CalculateScore(DealerHand)[1] < 17: # Dealer stops receiving cards at hard 17
      DealerHand.append(DealCard())
      display()
      
def playBlackjack():
  # Game Logic
  global GameActive
  # Make Deck
  if len(DealersDeck) == 0:
    DealerDeckShuffle()
  # Place Bets
  if PlayerWager == 0:
    PlaceBets()
  # Deal Opening Hand
  if len(PlayerHand) == 0:
    Opening()
  display() # Update Screen
  PlayerTurn()
  DealerTurn()
  display() # Update Screen
  if playerTurn is False and CalculateScore(DealerHand)[1] >= 17:
    GameActive = False
    pass

  if not GameActive:
    playAgain = ''
    # Show Results
    match DetermineResults():
      case 0:
        print("You are bust!")
      case 1: # Dealer busts with 22
        print('Dealer bust with 22, bets are pushed.')
        Payout(PlayerWager,3)
      case 2: # Dealer busts over 22
        print('Dealer bust over 22, you win!')
        if Blackjack(PlayerHand):
          Payout(PlayerWager,0)
        else:
          Payout(PlayerWager,1)
      case 3: # Tied
        print('Tied with the Dealer! Bets are pushed.')
        Payout(PlayerWager,3)
        pass
      case 4: # Dealer Wins
        print('Dealer wins')
        pass
      case 5: # 
        print('Your score is higher! You win!')
        if Blackjack(PlayerHand):
          Payout(PlayerWager,0)
        else:
          Payout(PlayerWager,1)
        pass
        
    while True:
      # Loop until a valid answer is received
      playAgain = input('Would you like to play again? [y/n] : ')
      # If the user inputs a correct answer, break loop and continue
      if playAgain.lower() == 'y':
        # If the user wants to play again, reactivate the Game, and clear hands
        GameActive = True
        ResetGame()
        break
      elif playAgain.lower() == 'n':
        ResetGame()
        break
      else:
        clear()
        print('Please input a valid option')
      

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
        while True:
          GameActive = True
          playBlackjack()
          if not GameActive:
            break
      case '2':
        print()
      case '3':
        MenuActive = False
        ProgramActive = False
        print('Thanks for playing!')
      case _:
        print("Please enter a valid input.")