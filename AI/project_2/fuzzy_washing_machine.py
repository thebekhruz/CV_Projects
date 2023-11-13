import sys
from typing import List
from frules.rules import Rule as FuzzySet
from frules.expressions import Expression as MemFunction
from frules.expressions import ltrapezoid, trapezoid, rtrapezoid


# membership functions and corresponding fuzzy sets for how dirty (in tablespoons)
almost_clean_fn = MemFunction(ltrapezoid(0.25, 1.00), "almost_clean")
almost_clean_set = FuzzySet(value=almost_clean_fn)

dirty_fn = MemFunction(rtrapezoid(0.50, 1.0), "dirty")
dirty_set = FuzzySet(value=dirty_fn)
# membership functions and corresponding fuzzy sets for how delicate (in fabric weight)
very_delicate_fn = MemFunction(ltrapezoid(2.00, 4.00), "very_delicate")
very_delicate_set = FuzzySet(value=very_delicate_fn)

delicate_fn = MemFunction(trapezoid(3.00, 4.00, 6.00, 7.00), "delicate")
delicate_set = FuzzySet(value=delicate_fn)

not_delicate_fn = MemFunction(rtrapezoid(6.00, 7.00), "not_delicate")
not_delicate_set = FuzzySet(value=not_delicate_fn)

# dictionary with the output level for each of the rules; the key pertains to the rule number
rule_weights_dict = {1:10, 2:40, 3:60, 4:100}

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# TASK 1: 2 marks
# Implement the function that computes the degree to which a crisp input belongs to a fuzzy set
#  Outputs how dirty is a set,
def fuzzify(fuzzy_set: FuzzySet, val: float) -> float:
#    eval is used to evaluate the value on the graph/. 
	return fuzzy_set.eval(value = val)


# TASK 2a: 2 marks
# Implement the function for computing the conjunction of a rule's antecedents
def get_conjunction(fuzzified_dirt: float, fuzzified_fabric_weight: float) -> float:
    return min(fuzzified_dirt,fuzzified_fabric_weight)
	# AND
	# this might be a problem. 

# TASK 2b: 2 marks
# Implement the function for computing the disjunction of a rule's antecedents
def get_disjunction(fuzzified_dirt: float, fuzzified_fabric_weight: float) -> float:
    return max(fuzzified_dirt,fuzzified_fabric_weight)
		# OR
		# this might be a problem. 



# TASK 3: 3 marks
# Implement the function for computing the combined value of a rule antecedent
def get_rule_antecedent_value(ant1: FuzzySet, val1: float, ant2: FuzzySet, val2: float, operator: str) -> float:
    if(operator == ""):
        x = fuzzify(ant2,val2)
        return x
    elif(operator == "AND"):
        x = fuzzify(ant1,val1)
        y = fuzzify(ant2,val2)
        return get_conjunction(x,y)
    elif(operator == "OR"):
        x = fuzzify(ant1,val1)
        y = fuzzify(ant2,val2)
        return get_disjunction(x,y)
#  what if you pass arguments like this get_rule_antecedent_value(very_delicate_set, value, None, 0.0) will it work?


# TASK 4: 2 marks
# Implement function that returns the weighted output level of a rule
def get_rule_output_value(rule_number: int, rule_antecedent_value: float) -> float:
	return rule_weights_dict.get(rule_number) * rule_antecedent_value


# TASK 5: 3 marks
# dirt_amount can range from 0 to 2.5 inclusive
# fabric_weight range from 1.0 to 11.00 inclusive
def configure_washing_machine(dirt_amount: float, fabric_weight: float) -> tuple:
    all_antecedents = [] # this should be set to a List containing the antecedent values for all rules
    all_outputs = [] # this should be set to a List containing the output values for all rules
 
 
    r1 = get_rule_antecedent_value(None, 0.0, very_delicate_set, fabric_weight, "")
    r2 = get_rule_antecedent_value(delicate_set, fabric_weight, almost_clean_set, dirt_amount, "OR" )
    r3 = get_rule_antecedent_value(delicate_set, fabric_weight, dirty_set, dirt_amount, "AND" )
    r4 = get_rule_antecedent_value(not_delicate_set, fabric_weight, dirty_set, dirt_amount, "AND" )
    
    all_antecedents.append(r1)
    all_antecedents.append(r2)
    all_antecedents.append(r3)
    all_antecedents.append(r4)
    
    o1 = get_rule_output_value(1,r1)
    o2 = get_rule_output_value(2,r2)
    o3 = get_rule_output_value(3,r3)
    o4 = get_rule_output_value(4,r4)
    
    all_outputs.append(o1)
    all_outputs.append(o2)
    all_outputs.append(o3)
    all_outputs.append(o4)
    return (all_antecedents, all_outputs)


# TASK 6: 3 marks
# Implement function that computes the weighted average over all rules
def get_weighted_average(all_antecedents: List, all_outputs: List) -> float:
	sum_outputs =0
	sum_antecedents =0

	for i in all_outputs:
		sum_outputs = sum_outputs + i
  
	for j in all_antecedents:
		sum_antecedents = sum_antecedents + j

	# result = sum_outputs / sum_antecedents
	return sum_outputs/sum_antecedents


# TASK 7: 3 marks
# Implement function for computing the actual temperature the machine should be set to
def get_temperature(all_antecedents: List, all_outputs: List) -> float:
    x = get_weighted_average(all_antecedents, all_outputs)
    result = 0.8*x+10
    return result
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Debug
if __name__ == '__main__':
	if len(sys.argv) > 2:
		cmd = "{}({})".format(sys.argv[1], ",".join(sys.argv[2:]))
		print("debug run:", cmd)
		ret = eval(cmd)
		print("ret value:", ret)
	else:
		sys.stderr.write("Usage: fuzzy_washing_machine.py FUNCTION ARG...")
		sys.exit(1)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# vim:set noet ts=4 sw=4:
