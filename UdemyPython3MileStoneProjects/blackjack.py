#deck and player are classes 
#play have attribute of wager, total_money,cards on hand;play have methods of hit and stand
#deck has attributes of card items, card values, card being dealt
import random


suits = ['Hearts', 'Diamonds', 'Spades', 'Clubs']
ranks = ['Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace']
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,'Queen':10, 'King':10, 'Ace':11}


#bool to test if player still wants to play the game
user_playing_game=True

class Player:
	def __init__(self,total_money,wager=0):
		self.total_money=total_money
		self.hand=[]
		self.wager=wager
		self.value=0
	def is_dealer(self):
		return self.total_money==0

#Override from the parent Player class to set the total on hand money as 0 also check if the dealer has reached 17
class Dealer(Player):
	def __init__(self,total_money=0,wager=0):
		self.total_money=total_money
		self.hand=[]
		self.wager=wager
		self.value=0
	def up_card(self):
		return self.hand[0]
	def hole_card(self):
		return self.hand[1]
	def dealer_17(self):
		if self.value>=17:
			print ('dealer has reached 17,dealer will stop dealing')
			return True
		else:
			return False

class Deck:
	def __init__(self):
		self.deck=[]
		for suit in suits:
			for rank in ranks:
				card=Card(suit,rank)
				self.deck.append(card)
	def __str__(self):
		deck_ls=[str(card) for card in self.deck]
		return ', '.join(deck_ls)

	def count(self):
		return len(self.deck)

	def shuffle(self):
		random.shuffle(self.deck)

	def deal(self):
		dealt_card=self.deck.pop()
		return dealt_card

class Card:
	def __init__(self,suit,rank):
		self.suit=suit
		self.rank=rank
		self.value=values[self.rank]
	def __str__(self):
		return '%s of %s' %(self.rank,self.suit)

def take_bet(player):
	bet=0
	while True:
		try:
			bet=int(input('take your bet: '))
			money=player.total_money
			while bet>money:
				print (f'put down a wager less than {money}')
				bet=int(input('take your bet: '))
			player.wager=bet
			break
		except:
			print('type in an integer')
			continue
	print (f'you have made a bet for ${bet}')		
	return bet

def hit(player,deck):
	card=deck.deal()
	player.hand.append(card)
	card_value=card.value
	player_value=player.value
	#if hit is executed by a dealer, then the dealer needs to stop at 17
	if player.is_dealer():
		if not player.dealer_17():
			player.value+=card_value
	#if hit executed by a player, check if player will bust when the card is ACE, ACE value is assigned to 1
	else:
		if card_value ==11 and player_value>10:
			card_value=1
		player.value+=card_value
	return card


def black_jack(player):
	if player.value==21:
		return True
	else:
		return False

def bust(player):
	if player.value>21:
		return True
	else:
		return False

def check_win(player,dealer):
	player_value=player.value
	dealer_value=dealer.value
	if player_value>dealer_value:
		return 'Y'
	elif player_value<dealer_value:
		return 'N'
	else:
		return 'T'

def player_win(player):
	wager=player.wager
	player.total_money+=wager
	print (f'congrats, you won the game. your total money has increased to {player.total_money}')

def player_lose(player):
	wager=player.wager
	player.total_money-=wager
	print (f'sorry you lost the game. your total money has reduced to {player.total_money}')

def choose_hit(option):
	user_option=option
	while user_option !='hit' and user_option!='stand':
		print ('wrong input. you can only type in hit or stand.')
		user_option = input ('do you wish to hit or stand: ')
	if user_option =='hit':
		print ('you choose to hit')
		return True
	else:
		print ('you choose to stand, dealer will stop dealing')
		return False

def show_one_card(card):
	print (f'card dealt is {card}')

def show_all_cards(player):
	card_ls=[str(card) for card in player.hand]
	cards=' and '.join(card_ls)
	print (f'the cards on your hand is {cards}')
	print (f'the total rank of your cards is {player.value}')

def user_play_game():
	result = True
	while result:
		user_response = input('would you like to play another game, Y or N:')
		if user_response =='N':
			print ('you\'ll exit the game')
			result = False
			break
		elif user_response!='Y':
			print ('wrong input, only Y or N.')
			continue
		else:
			print ('you\'ll play again')
			break
	return result


#Create a deck of 52 cards
deck=Deck()
deck.shuffle()


#Ask the Player for available money and their bet，Make sure that the Player's bet does not exceed their available chips
available_money=int(input('How much chips do you have with you: '))

while user_playing_game:
	player1=Player(available_money)
	bet=take_bet(player1)

	#Deal two cards to the Dealer and two cards to the Player
	dealer=Dealer()
	for d in range (2):
		hit (dealer,deck)

	for c in range(2):
		hit(player1,deck)

	#Show only one of the Dealer's cards, the other remains hidden
	print (f'dealer has a card of {str(dealer.up_card())}, and the other card is hidden. His up_card value is {values[dealer.up_card().rank]}')

	#Show both of the Player's cards
	show_all_cards(player1)
	#bool to test if player is still in the game with dealer
	playing = True

	while playing:
		##player has a blackjack, player wins
		if black_jack(player1):
			print ('You have a BlackJack!')
			player_win(player1)
			playing = False
			break
			#？game over here

		#player bust, player lose
		elif bust(player1):
			
			print ('You hand is busted.')
			player_lose(player1)
			playing = False
			break
			#？game over here

		else:	
			#If the Player's hand doesn't Bust (go over 21) and didn't have blackjack, keep asking if they'd like to Hit or stand
			player_option = input ('do you wish to hit or stand: ')
			if choose_hit(player_option):
				card=hit(player1,deck)
				show_one_card(card)
				show_all_cards(player1)
				continue
			else:
				print ('player has chosen stand, now dealer can hit')
				print(f'the hidden card of dealer is {str(dealer.hole_card())},and total rank of dealer\'s cards is {dealer.value}')
				playing = False
				#If a Player Stands, play the Dealer's hand. The dealer will always hit until the Dealer's value meets or exceeds 17
				while not dealer.dealer_17():
					card=hit(dealer,deck)
					show_one_card(card)
					show_all_cards(dealer)

			#now neither player and dealer is not playing anymore, check the card value between dealer and player
			print('dealer has stopped dealing, compare your ranks')
			print('for dealer:')
			show_all_cards(dealer)
			print('for player:')
			show_all_cards(player1)
			if bust(dealer):
				print('dealer busts. player wins.')
				player_win(player1)
			else:
				result = check_win(player1,dealer)
				if result =='Y':
					player_win(player1)
				elif result =='N':
					player_lose(player1)
				else:
					print ('it\'s a tie, you can keep your wager')

	available_money=player1.total_money

	#ask player if he wants to play again only if he still has money
	if player1.total_money>0:
		user_playing_game=user_play_game()
		continue
	else:
		print('you dont have any money to wager on left, good bye.')
		break

if player1.total_money>0:
	print(f'good game. you still have ${player1.total_money}')











		


	
	










