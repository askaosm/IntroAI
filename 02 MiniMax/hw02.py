from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

## Example Agent
class ReflexAgent(Agent):

  def Action(self, gameState):

    move_candidate = gameState.getLegalActions()

    scores = [self.reflex_agent_evaluationFunc(gameState, action) for action in move_candidate]
    bestScore = max(scores)
    Index = [index for index in range(len(scores)) if scores[index] == bestScore]
    get_index = random.choice(Index)

    return move_candidate[get_index]

  def reflex_agent_evaluationFunc(self, currentGameState, action):

    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = successorGameState.getPacmanPosition()
    oldFood = currentGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    return successorGameState.getScore()



def scoreEvalFunc(currentGameState):

  return currentGameState.getScore()

class AdversialSearchAgent(Agent):

  def __init__(self, getFunc ='scoreEvalFunc', depth ='2'):
    self.index = 0
    self.evaluationFunction = util.lookup(getFunc, globals())

    self.depth = int(depth)



class MinimaxAgent(AdversialSearchAgent):
  """
    [문제 01] MiniMaxAgent의 Action을 구현하시오.
    (depth와 evaluation function은 위에서 정의한 self.depth and self.evaluationFunction을 사용할 것.)
  """
  def Action(self, gameState):  
    ####################### Write Your Code Here ################################  
    def MaxValue(gameState,depth):
      if gameState.isWin() or gameState.isLose() or depth == self.depth:  
        return self.evaluationFunction(gameState), None
      #init
      actions = gameState.getLegalActions(0)
      bestAction = actions[0]
      value =float('-inf')  ## v=-∞
      #for loop about all acions to search good aciotn
      
      for action in actions:
        nextState=gameState.generateSuccessor(0,action)  #get next state
        newVal,_=MinValue(nextState, depth,1) #get the min val about next state
        
        if newVal>value:
          value=newVal
          bestAction=action
      return value, bestAction
    

    def MinValue(gameState,depth, agentIndex):
      if gameState.isWin() or gameState.isLose() or depth == self.depth:  
        return self.evaluationFunction(gameState), None
      #init
      actions=gameState.getLegalActions(agentIndex)
      value =float('inf')  ## v=∞
      bestAction=actions[0]
      
      #for loop about all acions to search good aciotn
      for action in actions:
        nextState=gameState.generateSuccessor(agentIndex,action)  #get next state
        
        if agentIndex== gameState.getNumAgents()-1:  #last gohast
          newVal, _ = MaxValue(nextState, depth + 1) 
        else:
          newVal,_=MinValue(nextState,depth,agentIndex+1)
        
      
        if newVal<value:
          value=newVal
          bestAction=action
      return value, bestAction
    _, bestAction = MaxValue(gameState, 0)
    return bestAction 
    
    ############################################################################




class AlphaBetaAgent(AdversialSearchAgent):
  """
    [문제 02] AlphaBetaAgent의 Action을 구현하시오.
    (depth와 evaluation function은 위에서 정의한 self.depth and self.evaluationFunction을 사용할 것.)
  """
  def Action(self, gameState):
    ####################### Write Your Code Here ################################

    def MaxValue(gameState,alpha ,beta ,depth):
      if gameState.isWin() or gameState.isLose() or depth == self.depth:  
        return self.evaluationFunction(gameState), None
      #init
      value =float('-inf')  ## v=-∞
      BestAction=None 
      
      #for loop about all acions to search good aciotn
      actions=gameState.getLegalActions(0)
      for action in actions:
        nextState=gameState.generateSuccessor(0,action)  #get next state
        newVal,_=MinValue(nextState, alpha,beta,depth,1) #get the min val about next state
        if newVal>value:
          value=newVal
          BestAction=action
        ##here is defferent from minimax
        if beta< value :  #the funal bacjed-up value of this Max node ->>>set ti uts aipha balue
          return value, BestAction
        alpha = max(alpha ,value) #update alpha
      return value, BestAction
    

    def MinValue(gameState,alpha,beta, depth, agentIndex):
      if gameState.isWin() or gameState.isLose() or depth == self.depth:  
        return self.evaluationFunction(gameState), None
      #init
      value =float('inf')  ## v=∞
      BestAction=None 
      
      #for loop about all acions to search good aciotn
      actions=gameState.getLegalActions(agentIndex)
      for action in actions:
        nextState=gameState.generateSuccessor(agentIndex,action)  #get next state
        if agentIndex== gameState.getNumAgents()-1:  #last gohast
          newVal, _ = MaxValue(nextState,alpha,beta, depth + 1) 
        else:
          newVal,_=MinValue(nextState,alpha,beta,depth,agentIndex+1)
        
      
        if newVal<value:
          value=newVal
          BestAction=action
        if value < alpha:
          return value, BestAction
        beta=min(beta,value)  #update beta
      return value, BestAction

    _, BestAction = MaxValue(gameState, float('-inf'), float('inf'), 0)
    return BestAction  #end action


    ############################################################################



class ExpectimaxAgent(AdversialSearchAgent):
  """
    [문제 03] ExpectimaxAgent의 Action을 구현하시오.
    (depth와 evaluation function은 위에서 정의한 self.depth and self.evaluationFunction을 사용할 것.)
  """
  def Action(self, gameState):
    ####################### Write Your Code Here ################################
    # def MaxValue(gameState,depth):
    #   if gameState.isWin() or gameState.isLose() or depth == self.depth:  
    #     return self.evaluationFunction(gameState), None
    #   actions=gameState.getLegalActions(0)
    #   return max(self.expceptValue)
     
      



    raise Exception("Not implemented yet")
    ############################################################################


   # def maxValue(gameState, depth):
            
        #     if gameState.isWin() or gameState.isLose() or depth == self.depth:   #game exit status 
        #         return self.evaluationFunction(gameState), None 

        #     actions=gameState.getLegalActions(0)
        #     if not actions: return self.evaluationFunction(gameState), None 
            
        #     #initialize -> firest action
        #     first_action=actions[0]
        #     firest_successor=gameState.generateSuccessor(0,first_action)
        #     value,_=minValue(firest_successor, depth,1)
        #     bestAction=first_action

        #     ##search max value action 1 to end
        #     for action in actions[1:]:
        #         successorState = gameState.generateSuccessor(0, action)
        #         newValue, _ = minValue(successorState, depth, 1) #
        #         if newValue > value: ##find out best value
        #             value=newValue
        #             bestAction=action
        #     return value, bestAction
      
        # def minValue(gameState, depth, agentIndex):
        #     if gameState.isWin() or gameState.isLose() or depth == self.depth:  
        #         return self.evaluationFunction(gameState), None

        #     actions=gameState.getLegalActions(agentIndex)
        #     if not actions: return self.evaluationFunction(gameState), None
           
        #     #init 
        #     first_action=actions[0]
        #     first_successor=gameState.generateSuccessor(agentIndex,first_action)
        #     if agentIndex== gameState.getNumAgents()-1:
        #         value, _ = maxValue(first_successor, depth+ 1)
        #     else:
        #         value, _ = minValue(first_successor, depth, agentIndex+1)
        #     bestAction = first_action

        #     ##search min aciont 1 to end
        #     for action in actions[1:] :
        #         successorState=gameState.generateSuccessor(agentIndex, action)
        #         if agentIndex==gameState.getNumAgents()-1:  
        #             newValue, _=maxValue(successorState, depth+1)
        #         else:
        #             newValue, _=minValue(successorState, depth, agentIndex + 1)

        #         if newValue<value:
        #             value= newValue
        #             bestAction= action
        #     return value, bestAction

        # _, bestAction=maxValue(gameState, 0)
        # return bestAction