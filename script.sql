/****** Object:  Database [sqldbndibalekeralynette01]    Script Date: 2/18/2025 4:27:26 PM ******/
CREATE DATABASE [sqldbndibalekeralynette01]  (EDITION = 'Standard', SERVICE_OBJECTIVE = 'S0', MAXSIZE = 250 GB) WITH CATALOG_COLLATION = SQL_Latin1_General_CP1_CI_AS, LEDGER = OFF;
GO
ALTER DATABASE [sqldbndibalekeralynette01] SET COMPATIBILITY_LEVEL = 160
GO
ALTER DATABASE [sqldbndibalekeralynette01] SET ANSI_NULL_DEFAULT OFF 
GO
ALTER DATABASE [sqldbndibalekeralynette01] SET ANSI_NULLS OFF 
GO
ALTER DATABASE [sqldbndibalekeralynette01] SET ANSI_PADDING OFF 
GO
ALTER DATABASE [sqldbndibalekeralynette01] SET ANSI_WARNINGS OFF 
GO
ALTER DATABASE [sqldbndibalekeralynette01] SET ARITHABORT OFF 
GO
ALTER DATABASE [sqldbndibalekeralynette01] SET AUTO_SHRINK OFF 
GO
ALTER DATABASE [sqldbndibalekeralynette01] SET AUTO_UPDATE_STATISTICS ON 
GO
ALTER DATABASE [sqldbndibalekeralynette01] SET CURSOR_CLOSE_ON_COMMIT OFF 
GO
ALTER DATABASE [sqldbndibalekeralynette01] SET CONCAT_NULL_YIELDS_NULL OFF 
GO
ALTER DATABASE [sqldbndibalekeralynette01] SET NUMERIC_ROUNDABORT OFF 
GO
ALTER DATABASE [sqldbndibalekeralynette01] SET QUOTED_IDENTIFIER OFF 
GO
ALTER DATABASE [sqldbndibalekeralynette01] SET RECURSIVE_TRIGGERS OFF 
GO
ALTER DATABASE [sqldbndibalekeralynette01] SET AUTO_UPDATE_STATISTICS_ASYNC OFF 
GO
ALTER DATABASE [sqldbndibalekeralynette01] SET ALLOW_SNAPSHOT_ISOLATION ON 
GO
ALTER DATABASE [sqldbndibalekeralynette01] SET PARAMETERIZATION SIMPLE 
GO
ALTER DATABASE [sqldbndibalekeralynette01] SET READ_COMMITTED_SNAPSHOT ON 
GO
ALTER DATABASE [sqldbndibalekeralynette01] SET  MULTI_USER 
GO
ALTER DATABASE [sqldbndibalekeralynette01] SET ENCRYPTION ON
GO
ALTER DATABASE [sqldbndibalekeralynette01] SET QUERY_STORE = ON
GO
ALTER DATABASE [sqldbndibalekeralynette01] SET QUERY_STORE (OPERATION_MODE = READ_WRITE, CLEANUP_POLICY = (STALE_QUERY_THRESHOLD_DAYS = 30), DATA_FLUSH_INTERVAL_SECONDS = 900, INTERVAL_LENGTH_MINUTES = 60, MAX_STORAGE_SIZE_MB = 100, QUERY_CAPTURE_MODE = AUTO, SIZE_BASED_CLEANUP_MODE = AUTO, MAX_PLANS_PER_QUERY = 200, WAIT_STATS_CAPTURE_MODE = ON)
GO
/*** The scripts of database scoped configurations in Azure should be executed inside the target database connection. ***/
GO
-- ALTER DATABASE SCOPED CONFIGURATION SET MAXDOP = 8;
GO
/****** Object:  Table [dbo].[restaurant_data]    Script Date: 2/18/2025 4:27:26 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[restaurant_data](
	[name] [nvarchar](100) NOT NULL,
	[address] [nvarchar](max) NULL,
	[cuisine] [nvarchar](50) NOT NULL,
	[rating] [float] NULL,
	[phone] [nvarchar](15) NULL,
	[website] [nvarchar](500) NULL,
	[id] [int] IDENTITY(1,1) NOT NULL,
 CONSTRAINT [PK_RESTAURANT_ID] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[search_history]    Script Date: 2/18/2025 4:27:26 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[search_history](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[user_id] [varchar](100) NOT NULL,
	[query] [varchar](200) NOT NULL,
	[timestamp] [datetime] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[SearchHistory]    Script Date: 2/18/2025 4:27:26 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[SearchHistory](
	[search_id] [int] IDENTITY(1,1) NOT NULL,
	[user_id] [int] NULL,
	[search_term] [nvarchar](100) NOT NULL,
	[latitude] [float] NOT NULL,
	[longitude] [float] NOT NULL,
	[radius] [int] NOT NULL,
	[limit] [int] NOT NULL,
	[search_timestamp] [datetime] NULL,
PRIMARY KEY CLUSTERED 
(
	[search_id] ASC
)WITH (STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[user_preference]    Script Date: 2/18/2025 4:27:26 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[user_preference](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[user_id] [varchar](100) NOT NULL,
	[preference] [varchar](200) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Users]    Script Date: 2/18/2025 4:27:26 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Users](
	[user_id] [int] IDENTITY(1,1) NOT NULL,
	[email] [nvarchar](100) NOT NULL,
	[preferences] [nvarchar](max) NULL,
	[username] [varchar](50) NOT NULL,
	[password_hash] [nvarchar](max) NULL,
	[favorite_cuisines] [nvarchar](max) NULL,
	[dietary_restrictions] [nvarchar](max) NULL,
	[created_at] [datetime] NULL,
	[updated_at] [datetime] NULL,
PRIMARY KEY CLUSTERED 
(
	[user_id] ASC
)WITH (STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY],
UNIQUE NONCLUSTERED 
(
	[email] ASC
)WITH (STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
ALTER TABLE [dbo].[SearchHistory] ADD  DEFAULT (getdate()) FOR [search_timestamp]
GO
ALTER TABLE [dbo].[Users] ADD  DEFAULT (getdate()) FOR [created_at]
GO
ALTER TABLE [dbo].[Users] ADD  DEFAULT (getdate()) FOR [updated_at]
GO
ALTER TABLE [dbo].[SearchHistory]  WITH CHECK ADD FOREIGN KEY([user_id])
REFERENCES [dbo].[Users] ([user_id])
GO
ALTER DATABASE [sqldbndibalekeralynette01] SET  READ_WRITE 
GO
