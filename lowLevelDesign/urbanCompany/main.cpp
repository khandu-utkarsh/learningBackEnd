//Requirement is to design a class system which can provide different types of services.

//Focus on two main services API
//1. API to create a new service like createService(string serviceId, string userId);
//2. API to get the last of past services like getServices(string userId);

enum ServiceType {
    CARPENTRY,
    ELECTRICIAN,
    CLEANING,
    PLUMBING
};

class Service {
protected:
    string serviceId;
    string userId;
    double price;
    string status;

public:
    Service(string serviceId, string userId) 
        : serviceId(serviceId), userId(userId), status("PENDING") {}
    
    virtual ~Service() = default;
    
    virtual void performService() = 0;
    
    string getServiceId() const { return serviceId; }
    string getUserId() const { return userId; }
    string getStatus() const { return status; }
    double getPrice() const { return price; }
};

class CarpentryService : public Service {
public:
    CarpentryService(string serviceId, string userId) 
        : Service(serviceId, userId) {
        price = 500.0; // Default price for carpentry
    }
    
    void performService() override {
        status = "IN_PROGRESS";
        // Specific carpentry logic here
        status = "COMPLETED";
    }
};

class ElectricianService : public Service {
public:
    ElectricianService(string serviceId, string userId) 
        : Service(serviceId, userId) {
        price = 400.0; // Default price for electrician
    }
    
    void performService() override {
        status = "IN_PROGRESS";
        // Specific electrician logic here
        status = "COMPLETED";
    }
};

class CleaningService : public Service {
public:
    CleaningService(string serviceId, string userId) 
        : Service(serviceId, userId) {
        price = 200.0; // Default price for cleaning
    }
    
    void performService() override {
        status = "IN_PROGRESS";
        // Specific cleaning logic here
        status = "COMPLETED";
    }
};

class PlumbingService : public Service {
public:
    PlumbingService(string serviceId, string userId) 
        : Service(serviceId, userId) {
        price = 300.0; // Default price for plumbing
    }
    
    void performService() override {
        status = "IN_PROGRESS";
        // Specific plumbing logic here
        status = "COMPLETED";
    }
};

//!This should be a singleton class, so that the whole of creation of a service responsibiltiy
//!lies with this class
class ServiceFactory {
private:
    unordered_map<string, vector<Service*>> userServices;

    ServiceFactory() {}
    ServiceFactory(const ServiceFactory&) = delete;
    ServiceFactory& operator=(const ServiceFactory&) = delete;

public:
    static ServiceFactory& getInstance() {
        static ServiceFactory instance;
        return instance;
    }

    Service* createService(string serviceId, string userId) {
        // Determine service type based on serviceId prefix
        string prefix = serviceId.substr(0, 2);
        Service* service = nullptr;
        
        if (prefix == "CP") {
            service = new CarpentryService(serviceId, userId);
        } else if (prefix == "EL") {
            service = new ElectricianService(serviceId, userId);
        } else if (prefix == "CL") {
            service = new CleaningService(serviceId, userId);
        } else if (prefix == "PL") {
            service = new PlumbingService(serviceId, userId);
        }
        
        if (service) {
            userServices[userId].push_back(service);
        }
        
        return service;
    }

    vector<Service*> getServices(string userId) {
        return userServices[userId];
    }

    ~ServiceFactory() {
        // Cleanup all services
        for (auto& userService : userServices) {
            for (Service* service : userService.second) {
                delete service;
            }
        }
    }
};

int main() {
    // Get the service factory instance
    ServiceFactory& factory = ServiceFactory::getInstance();
    
    // Example user IDs
    string user1 = "USER123";
    string user2 = "USER456";
    
    // Create different types of services for user1
    Service* carpentryService = factory.createService("CP001", user1);
    Service* electricianService = factory.createService("EL001", user1);
    
    // Create services for user2
    Service* cleaningService = factory.createService("CL001", user2);
    Service* plumbingService = factory.createService("PL001", user2);
    
    // Store all services in a vector for easy iteration
    vector<Service*> allServices = {
        carpentryService,
        electricianService,
        cleaningService,
        plumbingService
    };
    
    // Perform all services in a loop
    for (auto& service : allServices) {
        service->performService();
    }
    
    // Get and display services for each user
    vector<string> users = {user1, user2};
    for (const auto& userId : users) {
        cout << "\nServices for " << userId << ":" << endl;
        vector<Service*> userServices = factory.getServices(userId);
        for (const auto& service : userServices) {
            cout << "Service ID: " << service->getServiceId() 
                 << ", Status: " << service->getStatus()
                 << ", Price: $" << service->getPrice() << endl;
        }
    }
    
    return 0;
}


