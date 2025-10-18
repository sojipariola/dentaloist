# backend/app/utils/subscriptions.py

from ..models import SubscriptionPlan, db

# Cache for subscription plan limits to avoid database queries
_SUBSCRIPTION_LIMITS_CACHE = None

def _get_subscription_plan_limits():
    """Get subscription limits from the database and cache them"""
    global _SUBSCRIPTION_LIMITS_CACHE
    
    if _SUBSCRIPTION_LIMITS_CACHE is None:
        try:
            plans = SubscriptionPlan.query.filter_by(is_active=True).all()
            _SUBSCRIPTION_LIMITS_CACHE = {}
            for plan in plans:
                _SUBSCRIPTION_LIMITS_CACHE[plan.code] = {
                    'max_staff': plan.max_users or 0,
                    'max_patients': plan.max_patients or 0,
                    'price_monthly': float(plan.price_monthly) if plan.price_monthly else 0,
                    'price_yearly': float(plan.price_yearly) if plan.price_yearly else 0,
                    'features': plan.features or {},
                    'is_unlimited': plan.code == 'enterprise',
                    'plan_name': plan.name,
                    'plan_description': plan.description
                }
        except Exception:
            # If database is not available, use defaults
            _SUBSCRIPTION_LIMITS_CACHE = DEFAULT_SUBSCRIPTION_LIMITS
    
    return _SUBSCRIPTION_LIMITS_CACHE

def get_subscription_limits(plan_code):
    """Get subscription limits for a specific plan code"""
    limits_cache = _get_subscription_plan_limits()
    return limits_cache.get(plan_code, {
        'max_staff': 0,
        'max_patients': 0,
        'price_monthly': 0,
        'price_yearly': 0,
        'features': {},
        'is_unlimited': False,
        'plan_name': 'Unknown Plan',
        'plan_description': 'Plan not found'
    })

def can_add_staff(organization, current_count):
    """Check if organization can add more staff based on subscription"""
    if not organization or not organization.subscription:
        return False
    
    # Get the subscription plan code
    subscription_plan = organization.subscription.plan
    if isinstance(subscription_plan, SubscriptionPlan):
        plan_code = subscription_plan.code
    else:
        # If it's an ID, look up the plan
        try:
            plan = SubscriptionPlan.query.get(subscription_plan)
            plan_code = plan.code if plan else 'free'
        except Exception:
            plan_code = 'free'
    
    limits = get_subscription_limits(plan_code)
    
    # Enterprise plans have unlimited staff
    if limits.get('is_unlimited', False):
        return True
    
    limit = limits.get('max_staff', 0)
    return current_count < limit

def can_add_patient(organization, current_count):
    """Check if organization can add more patients based on subscription"""
    if not organization or not organization.subscription:
        return False
    
    # Get the subscription plan code
    subscription_plan = organization.subscription.plan
    if isinstance(subscription_plan, SubscriptionPlan):
        plan_code = subscription_plan.code
    else:
        # If it's an ID, look up the plan
        try:
            plan = SubscriptionPlan.query.get(subscription_plan)
            plan_code = plan.code if plan else 'free'
        except Exception:
            plan_code = 'free'
    
    limits = get_subscription_limits(plan_code)
    
    # Enterprise plans have unlimited patients
    if limits.get('is_unlimited', False):
        return True
    
    limit = limits.get('max_patients', 0)
    return current_count < limit

def can_add_family_member(user, current_count):
    """Check if user can add more family members based on subscription"""
    if not user or not user.organization:
        return False
    
    # Family members are typically limited across all plans
    # but higher plans get more family members
    try:
        subscription_plan = user.organization.subscription.plan
        if isinstance(subscription_plan, SubscriptionPlan):
            plan_code = subscription_plan.code
        else:
            plan = SubscriptionPlan.query.get(subscription_plan)
            plan_code = plan.code if plan else 'free'
    except Exception:
        plan_code = 'free'
    
    # Define family member limits per plan
    family_limits = {
        'free': 0,      # No family members for free plan
        'starter': 2,   # 2 family members for starter
        'professional': 5,  # 5 family members for professional
        'enterprise': 10   # 10 family members for enterprise
    }
    
    limit = family_limits.get(plan_code, 0)
    return current_count < limit

def get_family_member_limit(user):
    """Get the family member limit for a user based on their subscription plan"""
    if not user or not user.organization:
        return 0
    
    try:
        subscription_plan = user.organization.subscription.plan
        if isinstance(subscription_plan, SubscriptionPlan):
            plan_code = subscription_plan.code
        else:
            plan = SubscriptionPlan.query.get(subscription_plan)
            plan_code = plan.code if plan else 'free'
    except Exception:
        plan_code = 'free'
    
    family_limits = {
        'free': 0,
        'starter': 2,
        'professional': 5,
        'enterprise': 10
    }
    
    return family_limits.get(plan_code, 0)

def get_organization_limits(organization):
    """Get all limits for an organization"""
    if not organization or not organization.subscription:
        return get_subscription_limits('free')
    
    try:
        subscription_plan = organization.subscription.plan
        if isinstance(subscription_plan, SubscriptionPlan):
            plan_code = subscription_plan.code
        else:
            plan = SubscriptionPlan.query.get(subscription_plan)
            plan_code = plan.code if plan else 'free'
    except Exception:
        plan_code = 'free'
    
    return get_subscription_limits(plan_code)

def can_use_feature(organization, feature_name):
    """Check if organization can use a specific feature based on subscription"""
    if not organization or not organization.subscription:
        return False
    
    try:
        subscription_plan = organization.subscription.plan
        if isinstance(subscription_plan, SubscriptionPlan):
            plan_code = subscription_plan.code
        else:
            plan = SubscriptionPlan.query.get(subscription_plan)
            plan_code = plan.code if plan else 'free'
    except Exception:
        plan_code = 'free'
    
    limits = get_subscription_limits(plan_code)
    features = limits.get('features', {})
    
    # Check if feature is available in this plan
    return features.get(feature_name, False)

def get_available_features(organization):
    """Get all available features for an organization"""
    if not organization or not organization.subscription:
        return {}
    
    try:
        subscription_plan = organization.subscription.plan
        if isinstance(subscription_plan, SubscriptionPlan):
            plan_code = subscription_plan.code
        else:
            plan = SubscriptionPlan.query.get(subscription_plan)
            plan_code = plan.code if plan else 'free'
    except Exception:
        plan_code = 'free'
    
    limits = get_subscription_limits(plan_code)
    return limits.get('features', {})

def is_plan_active(organization):
    """Check if organization's subscription plan is active"""
    if not organization or not organization.subscription:
        return False
    
    return organization.subscription.is_active

def get_upgrade_options(current_organization):
    """Get available upgrade options for an organization"""
    if not current_organization or not current_organization.subscription:
        return []
    
    try:
        current_plan = current_organization.subscription.plan
        if isinstance(current_plan, SubscriptionPlan):
            current_plan_code = current_plan.code
        else:
            current_plan_obj = SubscriptionPlan.query.get(current_plan)
            current_plan_code = current_plan_obj.code if current_plan_obj else 'free'
        
        # Get all available plans
        all_plans = SubscriptionPlan.query.filter_by(is_active=True).order_by(
            SubscriptionPlan.price_monthly.asc()
        ).all()
        
        upgrade_options = []
        current_plan_found = False
        
        for plan in all_plans:
            if plan.code == current_plan_code:
                current_plan_found = True
                continue
            
            # Only show plans that are upgrades (higher price)
            if current_plan_found:
                upgrade_options.append({
                    'code': plan.code,
                    'name': plan.name,
                    'description': plan.description,
                    'price_monthly': float(plan.price_monthly) if plan.price_monthly else 0,
                    'price_yearly': float(plan.price_yearly) if plan.price_yearly else 0,
                    'max_staff': plan.max_users,
                    'max_patients': plan.max_patients,
                    'features': plan.features or {}
                })
        
        return upgrade_options
    except Exception:
        return []

def refresh_subscription_cache():
    """Refresh the subscription limits cache"""
    global _SUBSCRIPTION_LIMITS_CACHE
    _SUBSCRIPTION_LIMITS_CACHE = None

# Default subscription limits for testing/fallback
DEFAULT_SUBSCRIPTION_LIMITS = {
    'free': {
        'max_staff': 3,
        'max_patients': 10,
        'price_monthly': 0,
        'price_yearly': 0,
        'features': {
            'basic_features': True,
            'ai_advice': True,
            'patient_management': True,
            'appointment_scheduling': True
        },
        'is_unlimited': False,
        'plan_name': 'Free Plan',
        'plan_description': 'Basic features for small practices'
    },
    'starter': {
        'max_staff': 10,
        'max_patients': 100,
        'price_monthly': 49.99,
        'price_yearly': 499.99,
        'features': {
            'basic_features': True,
            'ai_advice': True,
            'patient_management': True,
            'appointment_scheduling': True,
            'advanced_features': True,
            'priority_support': True,
            'reporting': True
        },
        'is_unlimited': False,
        'plan_name': 'Starter Plan',
        'plan_description': 'Perfect for growing practices'
    },
    'professional': {
        'max_staff': 50,
        'max_patients': 500,
        'price_monthly': 149.99,
        'price_yearly': 1499.99,
        'features': {
            'basic_features': True,
            'ai_advice': True,
            'patient_management': True,
            'appointment_scheduling': True,
            'advanced_features': True,
            'priority_support': True,
            'reporting': True,
            'premium_features': True,
            '24/7_support': True,
            'analytics': True,
            'customization': True
        },
        'is_unlimited': False,
        'plan_name': 'Professional Plan',
        'plan_description': 'Advanced features for established practices'
    },
    'enterprise': {
        'max_staff': None,  # Unlimited
        'max_patients': None,  # Unlimited
        'price_monthly': 499.99,
        'price_yearly': 4999.99,
        'features': {
            'basic_features': True,
            'ai_advice': True,
            'patient_management': True,
            'appointment_scheduling': True,
            'advanced_features': True,
            'priority_support': True,
            'reporting': True,
            'premium_features': True,
            '24/7_support': True,
            'analytics': True,
            'customization': True,
            'all_features': True,
            'dedicated_support': True,
            'api_access': True,
            'white_label': True
        },
        'is_unlimited': True,
        'plan_name': 'Enterprise Plan',
        'plan_description': 'Unlimited features for large organizations'
    }
}

# Initialize with defaults - database will be loaded on first use
_SUBSCRIPTION_LIMITS_CACHE = None

'''
get_organization_limits() - Get all limits for an organization

can_use_feature() - Check specific feature access

get_available_features() - List all available features

is_plan_active() - Check subscription status

get_upgrade_options() - Show available upgrades

refresh_subscription_cache() - Manual cache refresh

'''