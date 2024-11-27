SELECT 'INITIALIZATION SCRIPT STARTING' as 'DEBUG';
SELECT NOW() as 'Start Time';

SELECT 'Waiting for migrations...' as 'DEBUG';
SELECT SLEEP(20);

SELECT 'Attempting to insert data...' as 'DEBUG';
INSERT IGNORE INTO ai_models (ai_model_id, model_name, description) 
VALUES 
    (1, 'GPT-3.5-turbo', 'OpenAI GPT-3.5モデル'),
    (2, 'GPT-4o', 'OpenAI GPT-4モデル'),
    (3, 'Claude-3-5-sonnet', 'Anthropic Claudeモデル')
ON DUPLICATE KEY UPDATE
    model_name = VALUES(model_name),
    description = VALUES(description);

SELECT 'Data insertion complete' as 'DEBUG';
SELECT NOW() as 'End Time';