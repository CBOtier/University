#include "GameScene.h"
#include "GameView.h"
#include <algorithm>
#include <float.h>
#include <math.h>

using sf::Keyboard;
using sf::Vector2f;
using sf::Vector2i;

static const float PLAYER_SPEED = 150.0f;
static const float JUMP_FORCE = 400.0f;
static const float GRAVITY = 800.0f;

static float velocityY = 0;
static bool canJump = false;

static Vector2f Normalize(const Vector2f& value)
{
    const float length = std::hypotf(value.x, value.y);
    if (length < FLT_EPSILON)
    {
        return Vector2f(0, 0);
    }
    return value / length;
}

static Vector2f Round(const Vector2f& value)
{
    return Vector2f(roundf(value.x), roundf(value.y));
}

GameScene* NewGameScene()
{
    GameScene* pLogic = new GameScene;
    TmxLevel& level = pLogic->level;

    if (!level.LoadFromFile("res/platformer.tmx"))
    {
        throw std::runtime_error("Failed to load map");
    }

    pLogic->player = level.GetFirstObject("player");
    pLogic->coins = level.GetAllObjects("coin");
    pLogic->enemies = level.GetAllObjects("enemy");
    pLogic->blocks = level.GetAllObjects("block");
    pLogic->startPosition = pLogic->player.sprite.getPosition();

    return pLogic;
}

void UpdateGameScene(void* pData, GameView& view, float deltaSec)
{
    GameScene* pLogic = reinterpret_cast<GameScene*>(pData);
    TmxObject& player = pLogic->player;

    // Движение по горизонтали
    Vector2f direction(0, 0);
    if (Keyboard::isKeyPressed(Keyboard::A) || Keyboard::isKeyPressed(Keyboard::Left))
    {
        direction.x = -1;
    }
    else if (Keyboard::isKeyPressed(Keyboard::D) || Keyboard::isKeyPressed(Keyboard::Right))
    {
        direction.x = +1;
    }

    // Прыжок
    if ((Keyboard::isKeyPressed(Keyboard::W) || Keyboard::isKeyPressed(Keyboard::Up)) && canJump)
    {
        velocityY = -JUMP_FORCE;
        canJump = false;
    }

	// Гравитация
    velocityY += GRAVITY * deltaSec;

    if (velocityY > 600.0f)
    {
        velocityY = 600.0f;
    }

    Vector2f movementX = Round(Vector2f(direction.x * PLAYER_SPEED * deltaSec, 0));
    Vector2f movementY = Round(Vector2f(0, velocityY * deltaSec));

	// Проверка столкновений по X
    bool hasXCollision = false;
    sf::FloatRect playerRect = player.sprite.getGlobalBounds();
    playerRect.left += movementX.x;

    for (const TmxObject& block : pLogic->blocks)
    {
        if (playerRect.intersects(block.rect))
        {
            hasXCollision = true;
            break;
        }
    }

    if (!hasXCollision)
    {
        player.MoveBy(movementX);
    }

	// Проверка столкновений по Y
    bool hasYCollision = false;
    playerRect = player.sprite.getGlobalBounds();
    playerRect.top += movementY.y;

    for (const TmxObject& block : pLogic->blocks)
    {
        if (playerRect.intersects(block.rect))
        {
            hasYCollision = true;

            if (velocityY > 0)
            {
                velocityY = 0;
                canJump = true;
            }
            else if (velocityY < 0)
            {
                velocityY = 0;
            }
            break;
        }
    }

    if (!hasYCollision)
    {
        player.MoveBy(movementY);
        canJump = false;
    }

	// Сбор монет
    for (auto it = pLogic->coins.begin(); it != pLogic->coins.end();)
    {
        if (player.sprite.getGlobalBounds().intersects(it->sprite.getGlobalBounds()))
        {
            it = pLogic->coins.erase(it);
        }
        else
        {
            ++it;
        }
    }

	// Столкновение с врагами
    for (const TmxObject& enemy : pLogic->enemies)
    {
        if (player.sprite.getGlobalBounds().intersects(enemy.sprite.getGlobalBounds()))
        {
            player.sprite.setPosition(pLogic->startPosition);
            velocityY = 0;
            canJump = false;
            break;
        }
    }

    const Vector2i windowSize = view.windowSize;
    SetCameraCenter(view, player.sprite.getPosition() + Vector2f(windowSize.x / 4, windowSize.y / 4));
}

void DrawGameScene(void* pData, GameView& view)
{
    GameScene* pLogic = reinterpret_cast<GameScene*>(pData);
    sf::RenderTarget& target = view.window;

    pLogic->level.Draw(target);

    for (const TmxObject& coin : pLogic->coins)
    {
        target.draw(coin.sprite);
    }
    for (const TmxObject& enemy : pLogic->enemies)
    {
        target.draw(enemy.sprite);
    }

    target.draw(pLogic->player.sprite);
}

void DestroyGameScene(GameScene*& pScene)
{
    delete pScene;
    pScene = nullptr;
}
