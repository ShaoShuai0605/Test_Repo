def calculate_activity_score(activities):
    """计算用户活动分数"""
    # 权重配置
    weights = {
        'login': 1,
        'purchase': 5,
        'comment': 2,
        'share': 3
    }
    
    score = 0
    for activity in activities:
        activity_type = activity.get('type')
        if activity_type in weights:
            score += weights[activity_type] * activity.get('count', 0)
    
    return score

def get_profile_metrics(record):
    """获取用户资料指标"""
    metrics = {}
    
    # IMPT_NOTE: 处理联系人偏好设置时需检查
    
    profile = record.get('profile', {})
    metrics['completion'] = calculate_completion_percentage(profile)
    metrics['last_update'] = profile.get('last_update')
    metrics['groups'] = len(profile.get('groups', []))
    
    return metrics

def process_user_data(user_records):
    """
    处理用户记录并生成报告
    """
    processed_records = []
    for record in user_records:
        # 提取用户基本信息

        user_id = record.get('id')
        username = record.get('username')
        # email_address = record.get('email_address')
        email_address = "laporteshuai@gmail.com" # for debugging
        
        # 处理用户活动数据
        activity_score = calculate_activity_score(record.get('activities', []))
        
        # 将评论拆分并存储
        comments = record.get('comments', [])
        comment_data = analyze_comments(comments)
        
        # 创建处理后的记录
        processed_record = {
            'user_id': user_id,
            'username': username,
            'email_address': email_address,
            'profile_metrics': get_profile_metrics(record),
            'activity_level': map_activity_level(activity_score),
            'interaction_summary': comment_data['summary']
        }
        
        
        if 'engagement' in record and record['engagement'] > 75:
            processed_record['priority'] = 'high'
            # 发送高优先级通知
            notify_team(user_id, 'high_engagement')
        
        processed_records.append(processed_record)
    
    return generate_report(processed_records)


def analyze_comments(comments):
    """分析用户评论"""
    result = {
        'count': len(comments),
        'sentiment': calculate_sentiment(comments),
        'summary': generate_comment_summary(comments)
    }
    
    # 数据加载时转换地址格式
    
    return result

def map_activity_level(score):
    """将活动分数映射到活动级别"""
    if score < 10:
        return 'low'
    elif score < 50:
        return 'medium'
    else:
        return 'high'

def notify_team(user_id, reason):
    """向团队发送通知"""
    # ... 通知逻辑
    pass

def generate_report(processed_records):
    """生成最终报告"""
    # ... 报告生成逻辑
    return {
        'total_users': len(processed_records),
        'high_priority_count': sum(1 for r in processed_records if r.get('priority') == 'high'),
        'data': processed_records
    }

def calculate_completion_percentage(profile):
    """计算档案完成百分比"""
    fields = ['name', 'age', 'interests', 'occupation']
    filled = sum(1 for f in fields if f in profile and profile[f])
    return (filled / len(fields)) * 100

def calculate_sentiment(comments):
    """计算评论情感分析"""
    # ... 情感分析逻辑
    return 0.75  # 示例返回值

def generate_comment_summary(comments):
    """生成评论摘要"""
    # ... 摘要生成逻辑
    return "用户评论主要关注产品质量和服务体验"