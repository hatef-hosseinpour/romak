class teskaServer:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'installersProject':
            return 'teska_server'
        return None
    
    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'installersProject':
            return 'teska_server'
        return None
    
    