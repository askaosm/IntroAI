import copy, queue

def standardize_variables(nonstandard_rules):
    '''
    @param nonstandard_rules (dict) - dict from ruleIDs to rules
        Each rule is a dict:
        rule['antecedents'] contains the rule antecedents (a list of propositions)
        rule['consequent'] contains the rule consequent (a proposition).
   
    @return standardized_rules (dict) - an exact copy of nonstandard_rules,
        except that the antecedents and consequent of every rule have been changed
        to replace the word "something" and "someone" with some variable name that is
        unique to the rule, and not shared by any other rule.
    @return variables (list) - a list of the variable names that were created.
        This list should contain only the variables that were used in rules.

    '''

    standardized_rules= copy.deepcopy(nonstandard_rules)
    count = 0
    variables = []

    for ruleID, rule in nonstandard_rules.items():
        for idx, antecedent in enumerate(rule['antecedents']):
            # antecedent가 리스트인지를 확인한다.
            if isinstance(antecedent, list):
                for i, item in enumerate(antecedent):
                    if isinstance(item, str) and ('something' in item or 'someone' in item):
                        newVar = 'x' + str(count).zfill(4) #고유한 변수명을 생성
                        variables.append(newVar)  #add the new variable
                        antecedent[i] = item.replace('something', newVar).replace('someone', newVar) #update
                        count += 1 
                standardized_rules[ruleID]['antecedents'][idx] = antecedent
            else:
                if isinstance(antecedent, str) and ('something' in antecedent or 'someone' in antecedent):
                    newVar = 'x' + str(count).zfill(4) #고유한 변수면을 생성
                    variables.append(newVar)  #add the new variable
                    standardized_rules[ruleID]['antecedents'][idx] = antecedent.replace('something', newVar).replace('someone', newVar) #update
                    count += 1

        result = rule['consequent'] #consequence에 대하여 
        if isinstance(result, str) and ('something' in result or 'someone' in result):
            newVar = 'x' + str(count).zfill(4)#고유한 변수면을 생성 
            variables.append(newVar) #add the new variable
            standardized_rules[ruleID]['consequent'] = result.replace('something', newVar).replace('someone', newVar)  #update
            count += 1


    return standardized_rules, variables

def unify(query, datum, variables):
    '''
    @param query: proposition that you're trying to match.
      The input query should not be modified by this function; consider deepcopy.
    @param datum: proposition against which you're trying to match the query.
      The input datum should not be modified by this function; consider deepcopy.
    @param variables: list of strings that should be considered variables.
      All other strings should be considered constants.
    
    Unification succeeds if (1) every variable x in the unified query is replaced by a 
    variable or constant from datum, which we call subs[x], and (2) for any variable y
    in datum that matches to a constant in query, which we call subs[y], then every 
    instance of y in the unified query should be replaced by subs[y].

    @return unification (list): unified query, or None if unification fails.
    @return subs (dict): mapping from variables to values, or None if unification fails.
       If unification is possible, then answer already has all copies of x replaced by
       subs[x], thus the only reason to return subs is to help the calling function
       to update other rules so that they obey the same substitutions.

    Examples:

    unify(['x', 'eats', 'y', False], ['a', 'eats', 'b', False], ['x','y','a','b'])
      unification = [ 'a', 'eats', 'b', False ]
      subs = { "x":"a", "y":"b" }
    unify(['bobcat','eats','y',True],['a','eats','squirrel',True], ['x','y','a','b'])
      unification = ['bobcat','eats','squirrel',True]
      subs = { 'a':'bobcat', 'y':'squirrel' }
    unify(['x','eats','x',True],['a','eats','a',True],['x','y','a','b'])
      unification = ['a','eats','a',True]
      subs = { 'x':'a' }
    unify(['x','eats','x',True],['a','eats','bobcat',True],['x','y','a','b'])
      unification = ['bobcat','eats','bobcat',True],
      subs = {'x':'a', 'a':'bobcat'}
      When the 'x':'a' substitution is detected, the query is changed to 
      ['a','eats','a',True].  Then, later, when the 'a':'bobcat' substitution is 
      detected, the query is changed to ['bobcat','eats','bobcat',True], which 
      is the value returned as the answer.
    unify(['a','eats','bobcat',True],['x','eats','x',True],['x','y','a','b'])
      unification = ['bobcat','eats','bobcat',True],
      subs = {'a':'x', 'x':'bobcat'}
      When the 'a':'x' substitution is detected, the query is changed to 
      ['x','eats','bobcat',True].  Then, later, when the 'x':'bobcat' substitution 
      is detected, the query is changed to ['bobcat','eats','bobcat',True], which is 
      the value returned as the answer.
    unify([...,True],[...,False],[...]) should always return None, None, regardless of the 
      rest of the contents of the query or datum.
    '''
  

    subs = {}
    unification = copy.deepcopy(query)

    if len(query) != len(datum):
        return None, None

    for i, (q, d) in enumerate(zip(query, datum)):
        if q in variables and d in variables:
            # both of query and datum is variable
            if q in subs:
                if subs[q] != d:
                    return None, None
                unification[i] = subs[q]
            elif d in subs:  #
                if subs[d] != q:
                    return None, None
                unification[i] = subs[d]
            else:
                subs[q] = d
                unification[i] = d
        elif q in variables:
            #only  q is variable
            if q in subs:
                if subs[q] != d:
                    return None, None
                unification[i] = subs[q]
            else:
                subs[q] = d
                unification[i] = d
        elif d in variables:
            # only d is varialbe
            if d in subs:
                if subs[d] != q:
                    return None, None
                unification[i] = subs[d]
            else:
                subs[d] = q
                unification[i] = q
        elif q != d:
            return None, None

    #unification concurrency
    for i, item in enumerate(unification):
        if item in subs:
            unification[i] = subs[item]

    return unification, subs

def apply(rule, goals, variables):
    '''
    @param rule: A rule that is being tested to see if it can be applied
      This function should not modify rule; consider deepcopy.
    @param goals: A list of propositions against which the rule's consequent will be tested
      This function should not modify goals; consider deepcopy.
    @param variables: list of strings that should be treated as variables

    Rule application succeeds if the rule's consequent can be unified with any one of the goals.
    
    @return applications: a list, possibly empty, of the rule applications that
       are possible against the present set of goals.
       Each rule application is a copy of the rule, but with both the antecedents 
       and the consequent modified using the variable substitutions that were
       necessary to unify it to one of the goals. Note that this might require 
       multiple sequential substitutions, e.g., converting ('x','eats','squirrel',False)
       based on subs=={'x':'a', 'a':'bobcat'} yields ('bobcat','eats','squirrel',False).
       The length of the applications list is 0 <= len(applications) <= len(goals).  
       If every one of the goals can be unified with the rule consequent, then 
       len(applications)==len(goals); if none of them can, then len(applications)=0.
    @return goalsets: a list of lists of new goals, where len(newgoals)==len(applications).
       goalsets[i] is a copy of goals (a list) in which the goal that unified with 
       applications[i]['consequent'] has been removed, and replaced by 
       the members of applications[i]['antecedents'].

    Example:
    rule={
      'antecedents':[['x','is','nice',True],['x','is','hungry',False]],
      'consequent':['x','eats','squirrel',False]
    }
    goals=[
      ['bobcat','eats','squirrel',False],
      ['bobcat','visits','squirrel',True],
      ['bald eagle','eats','squirrel',False]
    ]
    variables=['x','y','a','b']

    applications, newgoals = submitted.apply(rule, goals, variables)

    applications==[
      {
        'antecedents':[['bobcat','is','nice',True],['bobcat','is','hungry',False]],
        'consequent':['bobcat','eats','squirrel',False]
      },
      {
        'antecedents':[['bald eagle','is','nice',True],['bald eagle','is','hungry',False]],
        'consequent':['bald eagle','eats','squirrel',False]
      }
    ]
    newgoals==[
      [
        ['bobcat','visits','squirrel',True],
        ['bald eagle','eats','squirrel',False]
        ['bobcat','is','nice',True],
        ['bobcat','is','hungry',False]
      ],[
        ['bobcat','eats','squirrel',False]
        ['bobcat','visits','squirrel',True],
        ['bald eagle','is','nice',True],
        ['bald eagle','is','hungry',False]
      ]
    '''
    


    applications = []
    goalsets = []

    for goal in goals:
        
        unified, subs = unify(rule['consequent'], goal, variables)
        
        # If the unification is successful
        if unified:
            new_rule = copy.deepcopy(rule)  
            
            # Update the consequent
    
            updated_consequent = [subs.get(elem, elem) for elem in rule['consequent']]
            new_rule['consequent'] = updated_consequent
            
            # Update each antecedent 
           
            updated_antecedents = []
            for antecedent in rule['antecedents']:
              updated_antecedent = [subs.get(item, item) for item in antecedent]
              updated_antecedents.append(updated_antecedent)
              new_rule['antecedents'] = updated_antecedents

            # Add the modified rule to the applications list
            applications.append(new_rule)

            # Create a new set of goals
            new_goals = [g for g in goals if g != goal] 
            new_goals.extend(new_rule['antecedents'])  # Add the rule antecedents
            goalsets.append(new_goals)
            
    

    return applications, goalsets

def backward_chain(query, rules, variables):
    '''
    @param query: a proposition, you want to know if it is true
    @param rules: dict mapping from ruleIDs to rules
    @param variables: list of strings that should be treated as variables

    @return proof (list): a list of rule applications
      that, when read in sequence, conclude by proving the truth of the query.
      If no proof of the query was found, you should return proof=None.
    '''
    goals = [query]
    proof =[]

    while goals: 
      goal = goals.pop()
      for ruleID, rule in rules.items(): #goal가 각룰에 대해 적용가능한지 
        applications, new_goalsets=apply(rule, [goal],variables)
        if applications: #적용가능한 경우 proof에 추가한다. 
          selected_app=applications[0]
          proof.append(selected_app) #add the fisrst element of applications
          for new_goal in new_goalsets[0]:#
            goals.append(new_goal) ##add new goal
          break
      else:# if we can not proof return None
         return None
      
    return proof
