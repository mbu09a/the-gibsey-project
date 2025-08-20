"""QDPI Policy rules for narrative branching and return debt"""

# Configuration constants
MAX_RETURN_DEBT = 2
MAX_BRANCH_DEPTH = 3
MAX_OPEN_BRANCHES_PER_SECTION = 3

def allow_fork(open_branches: int, return_debt: int) -> bool:
    """
    Determine if a new narrative fork is allowed based on current state.
    
    Args:
        open_branches: Number of currently open branches in section
        return_debt: Current return debt (unresolved branches)
        
    Returns:
        True if fork is allowed, False otherwise
    """
    # Cannot fork if return debt is too high
    if return_debt > MAX_RETURN_DEBT:
        return False
    
    # Cannot fork if too many branches are already open
    if open_branches >= MAX_OPEN_BRANCHES_PER_SECTION:
        return False
        
    return True

def require_return(branch_length: int) -> bool:
    """
    Determine if a branch must return to canon based on its length.
    
    Args:
        branch_length: Number of pages in current branch
        
    Returns:
        True if return is required, False otherwise
    """
    return branch_length >= MAX_BRANCH_DEPTH

def calculate_trajectory_weight(
    trajectory: str,
    novelty: float,
    coherence: float,
    return_debt: int
) -> float:
    """
    Calculate weight/preference for a trajectory based on current state.
    
    Args:
        trajectory: T0, T1, T2, or T3
        novelty: Novelty score (0-1)
        coherence: Coherence score (0-1)
        return_debt: Current return debt
        
    Returns:
        Weight score for trajectory selection
    """
    base_weights = {
        "T0": 0.4,  # Continue within section
        "T1": 0.3,  # Loop back with bridge
        "T2": 0.2,  # Fork to new section
        "T3": 0.1   # Pure generative drift
    }
    
    weight = base_weights.get(trajectory, 0.0)
    
    # Adjust based on narrative state
    if trajectory == "T0":
        # Prefer continuation when coherence is high
        weight += coherence * 0.2
    elif trajectory == "T1":
        # Prefer loops when return debt is moderate
        if 0 < return_debt <= MAX_RETURN_DEBT:
            weight += 0.15
    elif trajectory == "T2":
        # Prefer forks when novelty is high and debt is low
        if return_debt == 0:
            weight += novelty * 0.2
        else:
            weight -= return_debt * 0.1
    elif trajectory == "T3":
        # Heavily penalize drift when debt exists
        weight -= return_debt * 0.15
        
    return max(0.0, min(1.0, weight))

def validate_transition(
    from_provenance: str,
    to_provenance: str,
    orientation: str
) -> bool:
    """
    Validate if a transition between provenances is allowed.
    
    Args:
        from_provenance: Current provenance (C/P/U/S)
        to_provenance: Target provenance
        orientation: Current orientation (X/Y/A/Z)
        
    Returns:
        True if transition is valid
    """
    # Canon can transition to anything
    if from_provenance == "C":
        return True
        
    # System can only transition to Canon or System
    if from_provenance == "S":
        return to_provenance in ["C", "S"]
        
    # User content must pass through Parallel before Canon
    if from_provenance == "U" and to_provenance == "C":
        return False
        
    # All other transitions allowed
    return True